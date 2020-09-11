import React from "react";
import { render } from "@testing-library/react";
import Logo from "./Logo";

test("Check if Logo is loaded", () => {
  const { getByText } = render(<Logo />);
  const linkElement = getByText("Boodschappp logo");
  expect(linkElement).toBeInTheDocument();
});
