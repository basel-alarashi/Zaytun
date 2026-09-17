export interface Category {
  id: number;
  name: string;
  slug: string;
}

export interface Unit {
  id: number;
  code: string;
}

export interface Product {
  id: number;
  name: string;
  description: string;
  price: string;          // DRF DecimalField serializes as string
  stock_quantity: number;
  is_active: boolean;
  is_available: boolean;
  category: Category;
  unit: Unit;
  farmer_id: number;
  farmer_name: string;
}

export interface ProductFormInput {
  name: string;
  description: string;
  price: string;
  stock_quantity: number;
  category: number;
  unit: number;
  is_active: boolean;
}

export interface FarmerStorefront {
  id: number;
  storefront_name: string;
  description: string;
  city: string;
  region: string;
  is_public: boolean;
}