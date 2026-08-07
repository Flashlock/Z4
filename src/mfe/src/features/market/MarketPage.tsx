import { useCallback, useEffect, useState } from "react";
import Accordion from "@mui/joy/Accordion";
import AccordionDetails from "@mui/joy/AccordionDetails";
import AccordionGroup from "@mui/joy/AccordionGroup";
import AccordionSummary from "@mui/joy/AccordionSummary";
import Box from "@mui/joy/Box";
import Button from "@mui/joy/Button";
import Input from "@mui/joy/Input";
import Sheet from "@mui/joy/Sheet";
import Typography from "@mui/joy/Typography";
import type { MarketProjection } from "../../api/types";
import { toUserMessage } from "../../api/errors";
import { fetchMarket, lockComponent } from "../../api/z4";
import { useToast } from "../../toast/ToastContext";
import { ListingCard } from "../build/ListingCard";
import { copper } from "../../theme";

export function MarketPage() {
  const toast = useToast();
  const [query, setQuery] = useState("");
  const [market, setMarket] = useState<MarketProjection | null>(null);
  const [busy, setBusy] = useState(false);

  const load = useCallback(
    async (q: string) => {
      setBusy(true);
      try {
        setMarket(await fetchMarket(q));
      } catch (err) {
        toast.error(toUserMessage(err, "fetchMarket failed"));
      } finally {
        setBusy(false);
      }
    },
    [toast],
  );

  useEffect(() => {
    void load("");
  }, [load]);

  const lock = async (componentId: number, listingId?: number) => {
    setBusy(true);
    try {
      await lockComponent(componentId, listingId);
      toast.success(listingId != null ? "Listing locked into master build." : "Component locked into master build.");
    } catch (err) {
      toast.error(toUserMessage(err, "lockComponent failed"));
    } finally {
      setBusy(false);
    }
  };

  return (
    <Box sx={{ p: 2.5, display: "grid", gap: 2 }}>
      <Sheet variant="outlined" sx={{ p: 2, backgroundColor: "background.surface" }}>
        <Typography level="body-xs" sx={{ color: copper, letterSpacing: "0.12em", textTransform: "uppercase", mb: 1 }}>
          Component market
        </Typography>
        <Box sx={{ display: "flex", gap: 1 }}>
          <Input
            sx={{ flex: 1 }}
            placeholder="Search components…"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") void load(query);
            }}
          />
          <Button size="sm" loading={busy} onClick={() => void load(query)}>
            Search
          </Button>
        </Box>
      </Sheet>

      <Sheet variant="outlined" sx={{ p: 2, backgroundColor: "background.surface" }}>
        <AccordionGroup>
          {(market?.groups ?? []).map((group) => (
            <Accordion key={group.component.id}>
              <AccordionSummary>
                <Box sx={{ display: "flex", justifyContent: "space-between", width: "100%", pr: 1, gap: 1 }}>
                  <Typography level="title-sm">
                    {group.component.manufacturer} {group.component.model}
                  </Typography>
                  <Typography level="body-xs" sx={{ color: "text.secondary", textTransform: "uppercase" }}>
                    {group.component.category} · {group.listings.length} listings
                  </Typography>
                </Box>
              </AccordionSummary>
              <AccordionDetails>
                <Box sx={{ display: "flex", justifyContent: "flex-end", mb: 1 }}>
                  <Button
                    size="sm"
                    variant="outlined"
                    loading={busy}
                    onClick={() => void lock(group.component.id)}
                  >
                    Lock component
                  </Button>
                </Box>
                {group.listings.map((listing) => (
                  <ListingCard
                    key={listing.id}
                    listing={listing}
                    busy={busy}
                    lockLabel="Lock listing"
                    onLock={() => void lock(group.component.id, listing.id)}
                  />
                ))}
              </AccordionDetails>
            </Accordion>
          ))}
        </AccordionGroup>
        {market && market.groups.length === 0 ? (
          <Typography level="body-sm" sx={{ color: "text.secondary" }}>
            No components match this search.
          </Typography>
        ) : null}
      </Sheet>
    </Box>
  );
}
