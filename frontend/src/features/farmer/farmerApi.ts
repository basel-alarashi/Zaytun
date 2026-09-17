import { apiClient } from "../../lib/apiClient";
import type { FarmerStorefront, Product, ProductFormInput, Category, Unit } from "../../types/catalog";

export const farmerApi = {
  getStorefront: () => apiClient.get<FarmerStorefront>("/farmers/me/storefront/"),
  updateStorefront: (data: Partial<FarmerStorefront>) =>
    apiClient.patch<FarmerStorefront>("/farmers/me/storefront/", data),

  listProducts: () => apiClient.get<Product[]>("/farmer/products/"),
  getProduct: (id: number) => apiClient.get<Product>(`/farmer/products/${id}/`),
  createProduct: (data: ProductFormInput) =>
    apiClient.post<Product>("/farmer/products/", data),
  updateProduct: (id: number, data: Partial<ProductFormInput>) =>
    apiClient.patch<Product>(`/farmer/products/${id}/`, data),
  deactivateProduct: (id: number) => apiClient.delete(`/farmer/products/${id}/`),

  listCategories: () => apiClient.get<Category[]>("/categories/"),
  listUnits: () => apiClient.get<Unit[]>("/units/"),
};