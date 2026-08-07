import { useCallback, useEffect, useState } from "react";
import Accordion from "@mui/joy/Accordion";
import AccordionDetails from "@mui/joy/AccordionDetails";
import AccordionGroup from "@mui/joy/AccordionGroup";
import AccordionSummary from "@mui/joy/AccordionSummary";
import Box from "@mui/joy/Box";
import Button from "@mui/joy/Button";
import Sheet from "@mui/joy/Sheet";
import Textarea from "@mui/joy/Textarea";
import Typography from "@mui/joy/Typography";
import type { HomeProjection } from "../../api/types";
import { toUserMessage } from "../../api/errors";
import { fetchHome, formatPrice, lockComponent, lockDraft, putGoal, unlockCategory } from "../../api/z4";
import { useToast } from "../../toast/ToastContext";
import { ListingCard } from "../build/ListingCard";
import { LockedSlotRow } from "../build/LockedSlotRow";
import { copper } from "../../theme";

export function HomePage() {
  const toast = useToast();
  const [home, setHome] = useState<HomeProjection | null>(null);
  const [goalText, setGoalText] = useState("");
  const [busy, setBusy] = useState(false);

  const refresh = useCallback(async () => {
    setBusy(true);
    try {
      const data = await fetchHome();
      setHome(data);
      setGoalText(data.goal.text);
    } catch (err) {
      toast.error(toUserMessage(err, "fetchHome failed"));
    } finally {
      setBusy(false);
    }
  }, [toast]);

  useEffect(() => {
    void refresh();
  }, [refresh]);

  const saveGoal = async () => {
    setBusy(true);
    try {
      await putGoal(goalText);
      const data = await fetchHome();
      setHome(data);
      setGoalText(data.goal.text);
    } catch (err) {
      toast.error(toUserMessage(err, "putGoal failed"));
    } finally {
      setBusy(false);
    }
  };

  const run = async (fn: () => Promise<HomeProjection>) => {
    setBusy(true);
    try {
      const data = await fn();
      setHome(data);
      setGoalText(data.goal.text);
    } catch (err) {
      toast.error(toUserMessage(err, "home action failed"));
    } finally {
      setBusy(false);
    }
  };

  return (
    <Box sx={{ p: 2.5, display: "grid", gap: 2 }}>
      <Sheet variant="outlined" sx={{ p: 2, backgroundColor: "background.surface" }}>
        <Typography level="body-xs" sx={{ color: copper, letterSpacing: "0.12em", textTransform: "uppercase", mb: 1 }}>
          Build goal
        </Typography>
        <Textarea
          minRows={3}
          value={goalText}
          onChange={(e) => setGoalText(e.target.value)}
          placeholder="e.g. Quiet 1440p editing rig under $1500"
        />
        <Box sx={{ mt: 1, display: "flex", justifyContent: "flex-end" }}>
          <Button size="sm" loading={busy} onClick={() => void saveGoal()}>
            Save goal
          </Button>
        </Box>
      </Sheet>

      <Sheet variant="outlined" sx={{ p: 2, backgroundColor: "background.surface" }}>
        <Box sx={{ display: "flex", justifyContent: "space-between", alignItems: "baseline", mb: 1 }}>
          <Typography level="body-xs" sx={{ color: copper, letterSpacing: "0.12em", textTransform: "uppercase" }}>
            Master build
          </Typography>
          <Typography level="title-sm">
            {home ? formatPrice(home.master.total_cents, home.master.currency) : "—"}
          </Typography>
        </Box>
        {!home || home.master.slots.length === 0 ? (
          <Typography level="body-sm" sx={{ color: "text.secondary" }}>
            No locked components yet. Lock parts from a draft or the market.
          </Typography>
        ) : (
          home.master.slots.map((slot) => (
            <LockedSlotRow
              key={slot.category}
              category={slot.category}
              component={slot.component}
              listing={slot.listing}
              busy={busy}
              onUnlock={() => void run(() => unlockCategory(slot.category))}
            />
          ))
        )}
      </Sheet>

      <Sheet variant="outlined" sx={{ p: 2, backgroundColor: "background.surface" }}>
        <Typography level="body-xs" sx={{ color: copper, letterSpacing: "0.12em", textTransform: "uppercase", mb: 1 }}>
          Top draft builds
        </Typography>
        <AccordionGroup>
          {(home?.drafts ?? []).map((draft) => (
            <Accordion key={draft.id}>
              <AccordionSummary>
                <Box sx={{ display: "flex", justifyContent: "space-between", width: "100%", pr: 1, gap: 1 }}>
                  <Typography level="title-sm">{draft.title}</Typography>
                  <Typography level="body-sm" sx={{ color: "text.secondary" }}>
                    {formatPrice(draft.total_cents, draft.currency)}
                  </Typography>
                </Box>
              </AccordionSummary>
              <AccordionDetails>
                <Box sx={{ display: "flex", justifyContent: "flex-end", mb: 1 }}>
                  <Button size="sm" loading={busy} onClick={() => void run(() => lockDraft(draft.id))}>
                    Lock entire build
                  </Button>
                </Box>
                {draft.slots.map((slot) =>
                  slot.listing ? (
                    <Box key={`${draft.id}-${slot.category}`}>
                      <Typography
                        level="body-xs"
                        sx={{ color: copper, letterSpacing: "0.08em", textTransform: "uppercase", mt: 1 }}
                      >
                        {slot.category}
                      </Typography>
                      <ListingCard
                        listing={slot.listing}
                        busy={busy}
                        onLock={() =>
                          void run(() => lockComponent(slot.component.id, slot.listing!.id))
                        }
                      />
                    </Box>
                  ) : null,
                )}
              </AccordionDetails>
            </Accordion>
          ))}
        </AccordionGroup>
      </Sheet>
    </Box>
  );
}
