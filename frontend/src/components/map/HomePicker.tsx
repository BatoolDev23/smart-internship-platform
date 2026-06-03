"use client";

import maplibregl, { type Map as MapLibreMap, type Marker as MarkerType } from "maplibre-gl";
import "maplibre-gl/dist/maplibre-gl.css";
import { useEffect, useRef } from "react";

const TILES =
  process.env.NEXT_PUBLIC_MAP_TILES ?? "https://tiles.openfreemap.org/styles/liberty";

export interface HomePickerProps {
  value: { lat: number; lng: number } | null;
  onChange: (coords: { lat: number; lng: number }) => void;
  height?: string;
  className?: string;
}

const JORDAN_CENTER: [number, number] = [36.2, 31.4];

export function HomePicker({ value, onChange, height = "320px", className }: HomePickerProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const mapRef = useRef<MapLibreMap | null>(null);
  const markerRef = useRef<MarkerType | null>(null);
  const onChangeRef = useRef(onChange);
  useEffect(() => {
    onChangeRef.current = onChange;
  }, [onChange]);

  useEffect(() => {
    if (!containerRef.current || mapRef.current) return;
    const start: [number, number] = value ? [value.lng, value.lat] : JORDAN_CENTER;
    const map = new maplibregl.Map({
      container: containerRef.current,
      style: TILES,
      center: start,
      zoom: value ? 11 : 7.2,
      attributionControl: { compact: true },
    });
    map.addControl(new maplibregl.NavigationControl({ showCompass: false }), "top-right");
    mapRef.current = map;

    const placeMarker = (lng: number, lat: number) => {
      if (markerRef.current) {
        markerRef.current.setLngLat([lng, lat]);
        return;
      }
      const el = document.createElement("div");
      el.style.cssText =
        "width:22px;height:22px;border-radius:9999px;background:linear-gradient(135deg,#ef4444,#f97316);box-shadow:0 0 0 4px rgba(239,68,68,0.35),0 4px 14px rgba(0,0,0,0.4);";
      markerRef.current = new maplibregl.Marker({ element: el, draggable: true })
        .setLngLat([lng, lat])
        .addTo(map);
      markerRef.current.on("dragend", () => {
        const ll = markerRef.current!.getLngLat();
        onChangeRef.current({ lat: ll.lat, lng: ll.lng });
      });
    };

    if (value) placeMarker(value.lng, value.lat);

    map.on("click", (e) => {
      placeMarker(e.lngLat.lng, e.lngLat.lat);
      onChangeRef.current({ lat: e.lngLat.lat, lng: e.lngLat.lng });
    });

    return () => {
      map.remove();
      mapRef.current = null;
      markerRef.current = null;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <div className={className} style={{ position: "relative", width: "100%", height }}>
      <div
        ref={containerRef}
        style={{ position: "absolute", inset: 0, borderRadius: "inherit", overflow: "hidden" }}
      />
    </div>
  );
}
