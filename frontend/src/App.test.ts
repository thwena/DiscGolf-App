import { describe, expect, it } from "vitest";
import { features } from "./App";

describe("Version 0.1 navigation", () => {
  it("keeps scoring, inventory, and Flight Lab in the first-release shell", () => {
    expect(features.map((feature) => feature.title)).toEqual([
      "Score a round",
      "Your bag",
      "Flight Lab"
    ]);
  });
});
