import { useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { farmerApi } from "../../features/farmer/farmerApi";
import { useAsync } from "../../hooks/useAsync";
import type { ProductFormInput, Product } from "../../types/catalog";
import type { ApiErrorPayload } from "../../types/errors";

const emptyForm: ProductFormInput = {
  name: "",
  description: "",
  price: "",
  stock_quantity: 0,
  category: 0,
  unit: 0,
  is_active: true,
};

function toFormInput(product: Product | null): ProductFormInput {
  if (!product) return emptyForm;
  return {
    name: product.name,
    description: product.description,
    price: product.price,
    stock_quantity: product.stock_quantity,
    category: product.category.id,
    unit: product.unit.id,
    is_active: product.is_active,
  };
}

interface ProductFormProps {
  isEdit: boolean;
  productId?: number;
  initial: Product | null;
  categories: { id: number; name: string }[] | null;
  units: { id: number; code: string }[] | null;
}

function ProductForm({ isEdit, productId, initial, categories, units }: ProductFormProps) {
  const navigate = useNavigate();
  // Initialize directly from `initial` — no effect, no mirroring.
  const [form, setForm] = useState<ProductFormInput>(() => toFormInput(initial));
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<ApiErrorPayload | null>(null);

  const handleSubmit = async (e: React.SubmitEvent<HTMLFormElement>) => {
    e.preventDefault();
    setSaving(true);
    setError(null);
    try {
      if (isEdit && productId !== undefined) {
        await farmerApi.updateProduct(productId, form);
      } else {
        await farmerApi.createProduct(form);
      }
      navigate("/farmer/products");
    } catch (err: unknown) {
      setError(
        (err as { payload?: ApiErrorPayload }).payload ?? {
          code: "UNKNOWN_ERROR",
          message: "Could not save product.",
        }
      );
    } finally {
      setSaving(false);
    }
  };

  const fieldError = (field: string) =>
    error?.details?.[field] ? String(error.details[field]) : null;

  return (
    <form onSubmit={handleSubmit} aria-labelledby="product-form-heading">
      <h1 id="product-form-heading">{isEdit ? "Edit product" : "New product"}</h1>

      {error && (
        <div role="alert" className="form-error">
          {error.message}
        </div>
      )}

      <label htmlFor="name">Name</label>
      <input
        id="name"
        value={form.name}
        onChange={(e) => setForm((f) => ({ ...f, name: e.target.value }))}
        required
      />

      <label htmlFor="description">Description</label>
      <textarea
        id="description"
        value={form.description}
        onChange={(e) => setForm((f) => ({ ...f, description: e.target.value }))}
      />

      <label htmlFor="price">Price</label>
      <input
        id="price"
        type="number"
        step="0.01"
        min="0.01"
        value={form.price}
        onChange={(e) => setForm((f) => ({ ...f, price: e.target.value }))}
        required
        aria-invalid={Boolean(fieldError("price"))}
      />
      {fieldError("price") && <p role="alert">{fieldError("price")}</p>}

      <label htmlFor="stock_quantity">Stock quantity</label>
      <input
        id="stock_quantity"
        type="number"
        min="0"
        value={form.stock_quantity}
        onChange={(e) =>
          setForm((f) => ({ ...f, stock_quantity: Number(e.target.value) }))
        }
        required
        aria-invalid={Boolean(fieldError("stock_quantity"))}
      />
      {fieldError("stock_quantity") && <p role="alert">{fieldError("stock_quantity")}</p>}

      <label htmlFor="category">Category</label>
      <select
        id="category"
        value={form.category || ""}
        onChange={(e) => setForm((f) => ({ ...f, category: Number(e.target.value) }))}
        required
      >
        <option value="" disabled>Select a category</option>
        {categories?.map((c) => (
          <option key={c.id} value={c.id}>{c.name}</option>
        ))}
      </select>

      <label htmlFor="unit">Unit</label>
      <select
        id="unit"
        value={form.unit || ""}
        onChange={(e) => setForm((f) => ({ ...f, unit: Number(e.target.value) }))}
        required
      >
        <option value="" disabled>Select a unit</option>
        {units?.map((u) => (
          <option key={u.id} value={u.id}>{u.code}</option>
        ))}
      </select>

      <label htmlFor="is_active">
        <input
          id="is_active"
          type="checkbox"
          checked={form.is_active}
          onChange={(e) => setForm((f) => ({ ...f, is_active: e.target.checked }))}
        />
        Active (orderable when in stock)
      </label>

      <button type="submit" disabled={saving}>
        {saving ? "Saving…" : isEdit ? "Save changes" : "Create product"}
      </button>
    </form>
  );
}

export function ProductFormPage() {
  const { id } = useParams<{ id?: string }>();
  const isEdit = Boolean(id);

  const { data: categories } = useAsync(() => farmerApi.listCategories(), []);
  const { data: units } = useAsync(() => farmerApi.listUnits(), []);
  const { data: existingProduct, loading: loadingProduct } = useAsync(
    () => (isEdit ? farmerApi.getProduct(Number(id)) : Promise.resolve(null)),
    [id]
  );

  if (isEdit && loadingProduct) return <p role="status">Loading product…</p>;

  // Keying the child by id ensures state resets if the route param changes.
  return (
    <ProductForm
      key={id ?? "new"}
      isEdit={isEdit}
      productId={id ? Number(id) : undefined}
      initial={existingProduct}
      categories={categories}
      units={units}
    />
  );
}