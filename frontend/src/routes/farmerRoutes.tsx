import type { RouteObject } from "react-router-dom";
import { RequireRole, type Role } from "../features/auth/RequireRole";
import { StorefrontEditorPage } from "../pages/farmer/StorefrontEditorPage";
import { ProductListPage } from "../pages/farmer/ProductListPage";
import { ProductFormPage } from "../pages/farmer/ProductFormPage";

const FARMER_ONLY: Role[] = ["FARMER"];

export const farmerRoutes: RouteObject[] = [
  {
    path: "/farmer/storefront",
    element: (
      <RequireRole allowedRoles={FARMER_ONLY}>
        <StorefrontEditorPage />
      </RequireRole>
    ),
  },
  {
    path: "/farmer/products",
    element: (
      <RequireRole allowedRoles={FARMER_ONLY}>
        <ProductListPage />
      </RequireRole>
    ),
  },
  {
    path: "/farmer/products/new",
    element: (
      <RequireRole allowedRoles={FARMER_ONLY}>
        <ProductFormPage />
      </RequireRole>
    ),
  },
  {
    path: "/farmer/products/:id/edit",
    element: (
      <RequireRole allowedRoles={FARMER_ONLY}>
        <ProductFormPage />
      </RequireRole>
    ),
  },
];