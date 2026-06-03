"use client";

import { AdminTable, Badge, PageHeader, confirmAction } from "@/components/admin/AdminTable";
import { Button } from "@/components/ui/Button";
import { api } from "@/lib/api";
import type { AdminUniversityRow } from "@/lib/types";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { ExternalLink, GraduationCap, Loader2, Plus, Trash2, X } from "lucide-react";
import { useEffect, useRef, useState } from "react";
import { toast } from "sonner";

// ─── Add University Modal ────────────────────────────────────────────────────

const inputCls =
  "w-full rounded-xl border border-[rgb(var(--border))] bg-[rgb(var(--background))] px-3.5 py-2.5 text-sm placeholder:text-[rgb(var(--muted))] focus:border-brand-500 focus:outline-none focus:ring-2 focus:ring-brand-500/25 transition-colors";

function AddUniversityModal({ open, onClose }: { open: boolean; onClose: () => void }) {
  const qc = useQueryClient();
  const overlayRef = useRef<HTMLDivElement>(null);
  const [form, setForm] = useState({
    name_en: "", name_ar: "", city: "Irbid", governorate: "Irbid",
    type: "public", website: "",
  });
  const [errors, setErrors] = useState<Record<string, string>>({});

  useEffect(() => {
    if (open) {
      setForm({ name_en: "", name_ar: "", city: "Irbid", governorate: "Irbid", type: "public", website: "" });
      setErrors({});
    }
  }, [open]);

  useEffect(() => {
    if (!open) return;
    const h = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", h);
    return () => window.removeEventListener("keydown", h);
  }, [open, onClose]);

  const mut = useMutation({
    mutationFn: (body: object) => api<AdminUniversityRow>("/admin/universities", { method: "POST", body }),
    onSuccess: () => {
      toast.success("Institute created ✓");
      qc.invalidateQueries({ queryKey: ["admin", "universities"] });
      qc.invalidateQueries({ queryKey: ["admin", "stats"] });
      onClose();
    },
    onError: (e: Error) => toast.error(e.message),
  });

  function validate() {
    const errs: Record<string, string> = {};
    if (!form.name_en.trim()) errs.name_en = "English name is required";
    if (!form.name_ar.trim()) errs.name_ar = "Arabic name is required";
    setErrors(errs);
    return Object.keys(errs).length === 0;
  }

  function submit(e: React.FormEvent) {
    e.preventDefault();
    if (!validate()) return;
    mut.mutate({ ...form, website: form.website || undefined });
  }

  const set = (k: string, v: string) => setForm((p) => ({ ...p, [k]: v }));

  if (!open) return null;
  return (
    <div ref={overlayRef} onClick={(e) => { if (e.target === overlayRef.current) onClose(); }}
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4">
      <div className="w-full max-w-lg rounded-3xl border border-[rgb(var(--border))] bg-[rgb(var(--background))] shadow-2xl">
        <div className="flex items-center justify-between border-b border-[rgb(var(--border))] px-6 py-4">
          <div className="flex items-center gap-3">
            <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-gradient-to-br from-brand-500 to-cyan-glow text-white">
              <GraduationCap className="h-4 w-4" />
            </div>
            <h2 className="font-bold">Add New Institute</h2>
          </div>
          <button onClick={onClose} className="flex h-8 w-8 items-center justify-center rounded-lg hover:bg-[rgb(var(--surface))] text-[rgb(var(--muted))]">
            <X className="h-4 w-4" />
          </button>
        </div>
        <form onSubmit={submit} className="p-6 space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-1.5">
              <label className="text-sm font-semibold">Name (English) <span className="text-rose-500">*</span></label>
              <input type="text" className={inputCls} value={form.name_en} onChange={(e) => set("name_en", e.target.value)} placeholder="Al-Balqa Applied University" />
              {errors.name_en && <p className="text-xs text-rose-500">{errors.name_en}</p>}
            </div>
            <div className="space-y-1.5">
              <label className="text-sm font-semibold">الاسم (عربي) <span className="text-rose-500">*</span></label>
              <input dir="rtl" type="text" className={inputCls} value={form.name_ar} onChange={(e) => set("name_ar", e.target.value)} placeholder="جامعة البلقاء التطبيقية" />
              {errors.name_ar && <p className="text-xs text-rose-500">{errors.name_ar}</p>}
            </div>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-1.5">
              <label className="text-sm font-semibold">City</label>
              <input type="text" className={inputCls} value={form.city} onChange={(e) => set("city", e.target.value)} />
            </div>
            <div className="space-y-1.5">
              <label className="text-sm font-semibold">Governorate</label>
              <input type="text" className={inputCls} value={form.governorate} onChange={(e) => set("governorate", e.target.value)} />
            </div>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-1.5">
              <label className="text-sm font-semibold">Type</label>
              <select className={inputCls} value={form.type} onChange={(e) => set("type", e.target.value)}>
                <option value="public">Public</option>
                <option value="private">Private</option>
              </select>
            </div>
            <div className="space-y-1.5">
              <label className="text-sm font-semibold">Website</label>
              <input type="url" className={inputCls} value={form.website} onChange={(e) => set("website", e.target.value)} placeholder="https://bau.edu.jo" />
            </div>
          </div>
          <div className="flex justify-end gap-2 pt-2 border-t border-[rgb(var(--border))]">
            <Button type="button" variant="outline" size="sm" onClick={onClose} disabled={mut.isPending}>Cancel</Button>
            <Button type="submit" size="sm" disabled={mut.isPending}>
              {mut.isPending ? <><Loader2 className="h-4 w-4 animate-spin" /> Saving…</> : <><Plus className="h-4 w-4" /> Add Institute</>}
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
}

// ─── Page ────────────────────────────────────────────────────────────────────

export default function AdminUniversitiesPage() {
  const qc = useQueryClient();
  const [showModal, setShowModal] = useState(false);
  const { data = [], isLoading } = useQuery({
    queryKey: ["admin", "universities"],
    queryFn: () => api<AdminUniversityRow[]>("/admin/universities"),
  });

  const del = useMutation({
    mutationFn: (id: number) => api<void>(`/admin/universities/${id}`, { method: "DELETE" }),
    onSuccess: () => {
      toast.success("Institute deleted");
      qc.invalidateQueries({ queryKey: ["admin"] });
    },
    onError: (e: Error) => toast.error(e.message),
  });

  return (
    <div>
      <PageHeader
        title="Institutes"
        subtitle="Universities and higher-education institutes registered on the platform"
        actions={
          <Button size="sm" onClick={() => setShowModal(true)} id="btn-add-university">
            <Plus className="h-4 w-4" /> Add Institute
          </Button>
        }
      />
      {isLoading ? (
        <div className="text-sm text-[rgb(var(--muted))]">Loading…</div>
      ) : (
        <AdminTable<AdminUniversityRow>
          rows={data}
          rowKey={(r) => r.id}
          searchPlaceholder="Search by name, city…"
          columns={[
            {
              key: "name_en",
              header: "Name",
              render: (r) => (
                <div>
                  <div className="font-medium">{r.name_en}</div>
                  <div className="text-xs text-[rgb(var(--muted))]">{r.name_ar}</div>
                </div>
              ),
            },
            { key: "type", header: "Type", render: (r) => <Badge tone={r.type === "public" ? "info" : "warn"}>{r.type}</Badge> },
            { key: "governorate", header: "Location", render: (r) => [r.city, r.governorate].filter(Boolean).join(", ") || "-" },
            { key: "students_count", header: "Students", render: (r) => <Badge tone="success">{r.students_count}</Badge> },
            {
              key: "website",
              header: "Website",
              render: (r) =>
                r.website ? (
                  <a href={r.website} target="_blank" rel="noreferrer"
                    className="inline-flex items-center gap-1 text-xs text-brand-600 dark:text-brand-300 hover:underline">
                    Visit <ExternalLink className="h-3 w-3" />
                  </a>
                ) : "-",
            },
            {
              key: "actions",
              header: "",
              searchable: false,
              className: "w-20",
              render: (r) => (
                <Button size="sm" variant="danger" disabled={del.isPending}
                  onClick={async () => {
                    if (await confirmAction(`Delete institute "${r.name_en}"? Linked students will be detached (not deleted).`)) {
                      del.mutate(r.id);
                    }
                  }}
                >
                  <Trash2 className="h-3.5 w-3.5" />
                </Button>
              ),
            },
          ]}
        />
      )}
      <AddUniversityModal open={showModal} onClose={() => setShowModal(false)} />
    </div>
  );
}
