import { Link } from "react-router-dom";
import { farmerApi } from "../../features/farmer/farmerApi";
import { useAsync } from "../../hooks/useAsync";

export function ProductListPage() {
  const { data: products, loading, error, refetch } = useAsync(
    () => farmerApi.listProducts(),
    []
  );

  const handleDeactivate = async (id: number) => {
    if (!window.confirm("Deactivate this product? It will no longer be orderable.")) return;
    try {
      await farmerApi.deactivateProduct(id);
      refetch();
    } catch {
      window.alert("Could not deactivate the product. Please try again.");
    }
  };

  if (loading) return <p role="status">Loading your products…</p>;

  if (error) {
    return (
      <div role="alert">
        <p>{error.message}</p>
        <button onClick={refetch}>Retry</button>
      </div>
    );
  }

  return (
    <div>
      <header>
        <h1>My Products</h1>
        <Link to="/farmer/products/new">Add product</Link>
      </header>

      {products && products.length === 0 ? (
        <p>You haven't listed any products yet.</p>
      ) : (
        <table>
          <thead>
            <tr>
              <th>Name</th>
              <th>Price</th>
              <th>Stock</th>
              <th>Status</th>
              <th aria-label="Actions" />
            </tr>
          </thead>
          <tbody>
            {products?.map((p) => (
              <tr key={p.id}>
                <td>{p.name}</td>
                <td>€{p.price}</td>
                <td>{p.stock_quantity}</td>
                <td>{p.is_active ? (p.is_available ? "Available" : "Out of stock") : "Inactive"}</td>
                <td>
                  <Link to={`/farmer/products/${p.id}/edit`}>Edit</Link>
                  {p.is_active && (
                    <button onClick={() => handleDeactivate(p.id)}>Deactivate</button>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}