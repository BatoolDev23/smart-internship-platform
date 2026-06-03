"use client";

import { AdminTable, Badge, PageHeader, confirmAction } from "@/components/admin/AdminTable";
import { Button } from "@/components/ui/Button";
import { api } from "@/lib/api";
import type { AdminUserRow } from "@/lib/types";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { Loader2, Plus, Power, Trash2, User, X } from "lucide-react";
import { useEffect, useRef, useState } from "react";
import { toast } from "sonner";

// ─── Add User Modal ──────────────────────────────────────────────────────────

const inputCls =
  "w-full rounded-xl border border-[rgb(var(--border))] bg-[rgb(var(--background))] px-3.5 py-2.5 text-sm placeholder:text-[rgb(var(--muted))] focus:border-brand-500 focus:outline-none focus:ring-2 focus:ring-brand-500/25 transition-colors";

function AddUserModal({ open, onClose }: { open: boolean; onClose: () => void }) {
  const qc = useQueryClient();
  const overlayRef = useRef<HTMLDivElement>(null);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [fullName, setFullName] = useState("");
  const [role, setRole] = useState("student");
  const [errors, setErrors] = useState<Record<string, string>>({});

  useEffect(() => {
    if (open) { setEmail(""); setPassword(""); setFullName(""); setRole("student"); setErrors({}); }
  }, [open]);

  useEffect(() => {
    if (!open) return;
    const h = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", h);
    return () => window.removeEventListener("keydown", h);
  }, [open, onClose]);

  const mut = useMutation({
    mutationFn: (body: object) => api<AdminUserRow>("/admin/users", { method: "POST", body }),
    onSuccess: () => {
      toast.success("User created ✓");
      qc.invalidateQueries({ queryKey: ["admin", "users"] });
      qc.invalidateQueries({ queryKey: ["admin", "stats"] });
      onClose();
    },
    onError: (e: Error) => toast.error(e.message),
  });

  function validate() {
    const errs: Record<string, string> = {};
    if (!email.trim()) errs.email = "Email is required";
    if (password.length < 8) errs.password = "Password must be at least 8 characters";
    setErrors(errs);
    return Object.keys(errs).length === 0;
  }

  function submit(e: React.FormEvent) {
    e.preventDefault();
    if (!validate()) return;
    mut.mutate({ email: email.trim(), password, role, full_name: fullName.trim() });
  }

  if (!open) return null;
  return (
    <div ref={overlayRef} onClick={(e) => { if (e.target === overlayRef.current) onClose(); }}
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4">
      <div className="w-full max-w-md rounded-3xl border border-[rgb(var(--border))] bg-[rgb(var(--background))] shadow-2xl">
        <div className="flex items-center justify-between border-b border-[rgb(var(--border))] px-6 py-4">
          <div className="flex items-center gap-3">
            <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-gradient-to-br from-brand-500 to-cyan-glow text-white">
              <User className="h-4 w-4" />
            </div>
            <h2 className="font-bold">Add New User</h2>
          </div>
          <button onClick={onClose} className="flex h-8 w-8 items-center justify-center rounded-lg hover:bg-[rgb(var(--surface))] text-[rgb(var(--muted))]">
            <X className="h-4 w-4" />
          </button>
        </div>
        <form onSubmit={submit} className="p-6 space-y-4">
          <div className="space-y-1.5">
            <label className="text-sm font-semibold">Email <span className="text-rose-500">*</span></label>
            <input type="email" className={inputCls} value={email} onChange={(e) => setEmail(e.target.value)} placeholder="user@example.com" />
            {errors.email && <p className="text-xs text-rose-500">{errors.email}</p>}
          </div>
          <div className="space-y-1.5">
            <label className="text-sm font-semibold">Full Name</label>
            <input type="text" className={inputCls} value={fullName} onChange={(e) => setFullName(e.target.value)} placeholder="Full name" />
          </div>
          <div className="space-y-1.5">
            <label className="text-sm font-semibold">Password <span className="text-rose-500">*</span></label>
            <input type="password" className={inputCls} value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Min. 8 characters" />
            {errors.password && <p className="text-xs text-rose-500">{errors.password}</p>}
          </div>
          <div className="space-y-1.5">
            <label className="text-sm font-semibold">Role</label>
            <select className={inputCls} value={role} onChange={(e) => setRole(e.target.value)}>
              <option value="student">Student</option>
              <option value="company">Company</option>
              <option value="admin">Admin</option>
            </select>
          </div>
          <div className="flex justify-end gap-2 pt-2 border-t border-[rgb(var(--border))]">
            <Button type="button" variant="outline" size="sm" onClick={onClose} disabled={mut.isPending}>Cancel</Button>
            <Button type="submit" size="sm" disabled={mut.isPending}>
              {mut.isPending ? <><Loader2 className="h-4 w-4 animate-spin" /> Saving…</> : <><Plus className="h-4 w-4" /> Add User</>}
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
}

// ─── Page ────────────────────────────────────────────────────────────────────

export default function AdminUsersPage() {
  const qc = useQueryClient();
  const [showModal, setShowModal] = useState(false);
  const { data = [], isLoading } = useQuery({
    queryKey: ["admin", "users"],
    queryFn: () => api<AdminUserRow[]>("/admin/users"),
  });

  const toggle = useMutation({
    mutationFn: (row: AdminUserRow) =>
      api<AdminUserRow>(`/admin/users/${row.id}/active`, {
        method: "PATCH",
        body: { is_active: !row.is_active },
      }),
    onSuccess: () => {
      toast.success("User status updated");
      qc.invalidateQueries({ queryKey: ["admin", "users"] });
      qc.invalidateQueries({ queryKey: ["admin", "stats"] });
    },
    onError: (e: Error) => toast.error(e.message),
  });

  const del = useMutation({
    mutationFn: (id: number) => api<void>(`/admin/users/${id}`, { method: "DELETE" }),
    onSuccess: () => {
      toast.success("User deleted");
      qc.invalidateQueries({ queryKey: ["admin"] });
    },
    onError: (e: Error) => toast.error(e.message),
  });

  return (
    <div>
      <PageHeader
        title="Users"
        subtitle="All registered accounts across the platform"
        actions={
          <Button size="sm" onClick={() => setShowModal(true)} id="btn-add-user">
            <Plus className="h-4 w-4" /> Add User
          </Button>
        }
      />
      {isLoading ? (
        <div className="text-sm text-[rgb(var(--muted))]">Loading…</div>
      ) : (
        <AdminTable<AdminUserRow>
          rows={data}
          rowKey={(r) => r.id}
          searchPlaceholder="Search by email, name, role…"
          columns={[
            { key: "id", header: "#", className: "w-12 text-[rgb(var(--muted))]" },
            {
              key: "email",
              header: "Email",
              render: (r) => (
                <div>
                  <div className="font-medium">{r.email}</div>
                  {r.full_name && <div className="text-xs text-[rgb(var(--muted))]">{r.full_name}</div>}
                </div>
              ),
            },
            {
              key: "role",
              header: "Role",
              render: (r) => (
                <Badge tone={r.role === "admin" ? "danger" : r.role === "company" ? "info" : "success"}>
                  {r.role}
                </Badge>
              ),
            },
            {
              key: "is_active",
              header: "Status",
              render: (r) => (
                <Badge tone={r.is_active ? "success" : "warn"}>
                  {r.is_active ? "Active" : "Disabled"}
                </Badge>
              ),
            },
            { key: "locale", header: "Locale", className: "uppercase" },
            {
              key: "actions",
              header: "Actions",
              searchable: false,
              className: "w-48",
              render: (r) => (
                <div className="flex items-center gap-2">
                  <Button
                    size="sm"
                    variant="outline"
                    onClick={() => toggle.mutate(r)}
                    disabled={toggle.isPending || r.role === "admin"}
                    title={r.is_active ? "Disable user" : "Enable user"}
                  >
                    <Power className="h-3.5 w-3.5" />
                    {r.is_active ? "Disable" : "Enable"}
                  </Button>
                  <Button
                    size="sm"
                    variant="danger"
                    disabled={del.isPending || r.role === "admin"}
                    onClick={async () => {
                      if (await confirmAction(`Delete user ${r.email}? This removes their applications and profile.`)) {
                        del.mutate(r.id);
                      }
                    }}
                  >
                    <Trash2 className="h-3.5 w-3.5" />
                  </Button>
                </div>
              ),
            },
          ]}
        />
      )}
      <AddUserModal open={showModal} onClose={() => setShowModal(false)} />
    </div>
  );
}
