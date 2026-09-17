import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MemoryRouter } from "react-router-dom";
import { vi, describe, it, expect, beforeEach } from "vitest";
import { ProductListPage } from "../ProductListPage";
import { farmerApi } from "../../../features/farmer/farmerApi";

vi.mock("../../../features/farmer/farmerApi");

const mockProducts = [
  {
    id: 1, name: "Tomatoes", price: "2.50", stock_quantity: 10,
    is_active: true, is_available: true,
    category: { id: 1, name: "Vegetables", slug: "vegetables" },
    unit: { id: 1, code: "kg" }, farmer_id: 1, farmer_name: "Farm A",
    description: "",
  },
];

describe("ProductListPage", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("shows a loading state then renders products", async () => {
    vi.mocked(farmerApi.listProducts).mockResolvedValue(mockProducts);
    render(<ProductListPage />, { wrapper: MemoryRouter });

    expect(screen.getAllByRole("status")[0]).toBeInTheDocument();
    await waitFor(() => expect(screen.getAllByText("Tomatoes")[0]).toBeInTheDocument());
  });

  it("shows an empty state when there are no products", async () => {
    vi.mocked(farmerApi.listProducts).mockResolvedValue([]);
    render(<ProductListPage />, { wrapper: MemoryRouter });

    await waitFor(() =>
      expect(screen.getAllByText(/haven't listed any products/i)[0]).toBeInTheDocument()
    );
  });

  it("shows an error state with retry on failure", async () => {
    vi.mocked(farmerApi.listProducts).mockRejectedValue({
      payload: { code: "SERVER_ERROR", message: "Could not load products." },
    });
    render(<ProductListPage />, { wrapper: MemoryRouter });

    await waitFor(() =>
      expect(screen.getAllByText("Could not load products.")[0]).toBeInTheDocument()
    );
    expect(screen.getAllByRole("alert")[0]).toBeInTheDocument();
  });

  it("deactivates a product after confirmation", async () => {
    vi.mocked(farmerApi.listProducts).mockResolvedValue(mockProducts);
    vi.mocked(farmerApi.deactivateProduct).mockResolvedValue(undefined);
    vi.spyOn(window, "confirm").mockReturnValue(true);

    render(<ProductListPage />, { wrapper: MemoryRouter });
    await waitFor(() => screen.getAllByText("Tomatoes")[0]);

    await userEvent.click(screen.getAllByRole("button", { name: /deactivate/i })[0]);

    await waitFor(() => expect(farmerApi.deactivateProduct).toHaveBeenCalledWith(1));
  });

  it("does not deactivate when confirmation is declined", async () => {
    vi.mocked(farmerApi.listProducts).mockResolvedValue(mockProducts);
    vi.spyOn(window, "confirm").mockReturnValue(false);

    render(<ProductListPage />, { wrapper: MemoryRouter });
    await waitFor(() => screen.getAllByText("Tomatoes")[0]);

    await userEvent.click(screen.getAllByRole("button", { name: /deactivate/i })[0]);

    expect(farmerApi.deactivateProduct).not.toHaveBeenCalled();
  });
});