import { useState } from "react";
import { farmerApi } from "../../features/farmer/farmerApi";
import { useAsync } from "../../hooks/useAsync";
import type { FarmerStorefront } from "../../types/catalog";
import type { ApiErrorPayload } from "../../types/errors";

interface StorefrontFormProps {
    initial: FarmerStorefront;
}

function StorefrontForm({ initial }: StorefrontFormProps) {
    // Initialize directly from the loaded entity — no effect required.
    const [form, setForm] = useState<Partial<FarmerStorefront>>(initial);
    const [saving, setSaving] = useState(false);
    const [saveError, setSaveError] = useState<ApiErrorPayload | null>(null);
    const [saved, setSaved] = useState(false);

    const handleSubmit = async (e: React.SubmitEvent) => {
        e.preventDefault();
        setSaving(true);
        setSaveError(null);
        setSaved(false);
        try {
            await farmerApi.updateStorefront(form);
            setSaved(true);
        } catch (err: unknown) {
            setSaveError(
                (err as { payload?: ApiErrorPayload }).payload ?? {
                    code: "UNKNOWN_ERROR",
                    message: "Could not save storefront.",
                }
            );
        } finally {
            setSaving(false);
        }
    };

    return (
        <form onSubmit={handleSubmit} aria-labelledby="storefront-heading">
            <h1 id="storefront-heading">My Storefront</h1>

            {saveError && (
                <div role="alert" className="form-error">
                    {saveError.message}
                    {typeof saveError.details?.storefront_name === 'string' && (
                        <p>{saveError.details.storefront_name}</p>
                    )}
                </div>
            )}
            {saved && <p role="status">Storefront updated.</p>}

            <label htmlFor="storefront_name">Storefront name</label>
            <input
                id="storefront_name"
                value={form.storefront_name ?? ""}
                onChange={(e) => setForm((f) => ({ ...f, storefront_name: e.target.value }))}
                required
            />

            <label htmlFor="description">Description</label>
            <textarea
                id="description"
                value={form.description ?? ""}
                onChange={(e) => setForm((f) => ({ ...f, description: e.target.value }))}
            />

            <label htmlFor="city">City</label>
            <input
                id="city"
                value={form.city ?? ""}
                onChange={(e) => setForm((f) => ({ ...f, city: e.target.value }))}
                required
            />

            <label htmlFor="region">Region</label>
            <input
                id="region"
                value={form.region ?? ""}
                onChange={(e) => setForm((f) => ({ ...f, region: e.target.value }))}
                required
            />

            <label htmlFor="is_public">
                <input
                    id="is_public"
                    type="checkbox"
                    checked={form.is_public ?? false}
                    onChange={(e) => setForm((f) => ({ ...f, is_public: e.target.checked }))}
                />
                Publish storefront (visible to consumers)
            </label>

            <button type="submit" disabled={saving}>
                {saving ? "Saving…" : "Save storefront"}
            </button>
        </form>
    );
}

export function StorefrontEditorPage() {
    const { data: storefront, loading, error, refetch } = useAsync(
        () => farmerApi.getStorefront(),
        []
    );

    if (loading) return <p role="status">Loading your storefront…</p>;

    if (error) {
        return (
            <div role="alert">
                <p>{error.message}</p>
                <button onClick={refetch}>Retry</button>
            </div>
        );
    }

    if (!storefront) return null;

    return <StorefrontForm initial={storefront} />;
}