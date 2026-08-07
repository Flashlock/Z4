import Box from "@mui/joy/Box";
import Button from "@mui/joy/Button";
import Typography from "@mui/joy/Typography";
import type { Component, Listing } from "../../api/types";
import { formatPrice } from "../../api/z4";
import { copper } from "../../theme";

interface Props {
  category: string;
  component: Component;
  listing?: Listing | null;
  onUnlock?: () => void;
  busy?: boolean;
}

export function LockedSlotRow({ category, component, listing, onUnlock, busy }: Props) {
  return (
    <Box
      sx={{
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        gap: 1,
        py: 1,
        borderBottom: "1px solid",
        borderColor: "neutral.outlinedBorder",
      }}
    >
      <Box>
        <Typography level="body-xs" sx={{ color: copper, letterSpacing: "0.08em", textTransform: "uppercase" }}>
          {category} · locked
        </Typography>
        <Typography level="title-sm">
          {component.manufacturer} {component.model}
        </Typography>
        {listing ? (
          <Typography level="body-xs" sx={{ color: "text.secondary" }}>
            via {listing.marketplace} · {formatPrice(listing.price_cents, listing.currency)}
          </Typography>
        ) : (
          <Typography level="body-xs" sx={{ color: "text.secondary" }}>
            Owned / no listing attached
          </Typography>
        )}
      </Box>
      {onUnlock ? (
        <Button size="sm" variant="outlined" color="neutral" loading={busy} onClick={onUnlock}>
          Unlock
        </Button>
      ) : null}
    </Box>
  );
}
