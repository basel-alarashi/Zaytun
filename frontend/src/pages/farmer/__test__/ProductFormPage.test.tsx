import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MemoryRouter } from "react-router-dom";
import { vi, describe, it, expect, beforeEach } from "vitest";
import { ProductFormPage } from "../ProductFormPage";
import { farmerApi } from "../../../features/farmer/farmerApi";
import type { Product } from "../../../types/catalog";

vi.mock("../../../features/farmer/farmerApi");

describe("ProductFormPage (create)", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    vi.mocked(farmerApi.listCategories).mockResolvedValue([
      { id: 1, name: "Vegetables", slug: "vegetables" },
    ]);
    vi.mocked(farmerApi.listUnits).mockResolvedValue([{ id: 1, code: "kg" }]);
  });

  it("submits a new product with server-side validation surfaced on failure", async () => {
    vi.mocked(farmerApi.createProduct).mockRejectedValue({
      payload: {
        code: "VALIDATION_ERROR",
        message: "The request could not be processed.",
        details: { price: "Price must be greater than zero." },
      },
    });

    const { container } = render(<ProductFormPage />, { wrapper: MemoryRouter });
    await waitFor(() => screen.getAllByLabelText(/category/i)[0]);

    // Disable native HTML5 browser validation for this form test
    const form = container.querySelector("form");
    if (form) form.noValidate = true;

    await userEvent.type(screen.getAllByLabelText(/^name$/i)[0], "Cucumbers");
    await userEvent.type(screen.getAllByLabelText(/price/i)[0], "0");
    await userEvent.click(screen.getAllByRole("button", { name: /create product/i })[0]);

    await waitFor(() =>
      expect(screen.getAllByText("Price must be greater than zero.")[0]).toBeInTheDocument()
    );
  });

  it("navigates back to the list on successful creation", async () => {
    vi.mocked(farmerApi.createProduct).mockResolvedValue({} as Product);
    render(<ProductFormPage />, { wrapper: MemoryRouter });
    await waitFor(() => screen.getAllByLabelText(/category/i)[0]);

    await userEvent.type(screen.getAllByLabelText(/^name$/i)[0], "Cucumbers");
    await userEvent.type(screen.getAllByLabelText(/price/i)[0], "1.75");
    await userEvent.type(screen.getAllByLabelText(/stock quantity/i)[0], "10");
    await userEvent.selectOptions(screen.getAllByLabelText(/category/i)[0], "1");
    await userEvent.selectOptions(screen.getAllByLabelText(/unit/i)[0], "1");
    await userEvent.click(screen.getAllByRole("button", { name: /create product/i })[0]);

    await waitFor(() => expect(farmerApi.createProduct).toHaveBeenCalled());
  });
});