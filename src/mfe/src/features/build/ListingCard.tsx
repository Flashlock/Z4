import Box from "@mui/joy/Box";
import Button from "@mui/joy/Button";
import Typography from "@mui/joy/Typography";
import type { Listing } from "../../api/types";
import { formatPrice } from "../../api/z4";

interface Props {
  listing: Listing;
  onLock?: () => void;
  lockLabel?: string;
  busy?: boolean;
}

export function ListingCard({ listing, onLock, lockLabel = "Lock", busy }: Props) {
  return (
    <Box
      sx={{
        display: "grid",
        gridTemplateColumns: "80px 1fr auto",
        gap: 1.5,
        alignItems: "center",
        py: 1,
        borderBottom: "1px solid",
        borderColor: "neutral.outlinedBorder",
      }}
    >
      <Box
        component="img"
        src={listing.image_url || "https://placehold.co/80x60/1E293B/475569?text=—"}
        alt=""
        sx={{ width: 80, height: 60, objectFit: "cover", backgroundColor: "background.level1" }}
      />
      <Box>
        <Typography level="title-sm">{listing.title}</Typography>
        <Typography level="body-xs" sx={{ color: "text.secondary" }}>
          {listing.marketplace} · {listing.seller} · {listing.condition} · reliability{" "}
          {listing.reliability_score.toFixed(1)}
        </Typography>
        <Typography level="body-sm" sx={{ mt: 0.5 }}>
          {formatPrice(listing.price_cents, listing.currency)}{" "}
          <Typography
            component="a"
            href={listing.listing_url}
            target="_blank"
            rel="noreferrer"
            level="body-xs"
            sx={{ color: "primary.500", ml: 1 }}
          >
            Purchase
          </Typography>
        </Typography>
      </Box>
      {onLock ? (
        <Button size="sm" loading={busy} onClick={onLock}>
          {lockLabel}
        </Button>
      ) : null}
    </Box>
  );
}
