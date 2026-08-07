import { NavLink, Outlet } from "react-router-dom";
import Box from "@mui/joy/Box";
import Typography from "@mui/joy/Typography";

const linkSx = {
  color: "text.secondary",
  textDecoration: "none",
  fontSize: "0.875rem",
  "&.active": { color: "primary.500" },
} as const;

export function Layout() {
  return (
    <Box
      sx={{
        minHeight: "100%",
        display: "flex",
        flexDirection: "column",
        backgroundColor: "background.body",
      }}
    >
      <Box
        component="header"
        sx={{
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          gap: 2,
          px: 2.5,
          py: 2,
          borderBottom: "1px solid",
          borderColor: "neutral.outlinedBorder",
        }}
      >
        <Box sx={{ display: "flex", alignItems: "baseline", gap: 1.5 }}>
          <Typography level="h3" sx={{ color: "primary.500", letterSpacing: "0.08em" }}>
            Z4
          </Typography>
          <Typography level="body-sm" sx={{ color: "text.secondary" }}>
            Autonomous engineering workstation
          </Typography>
        </Box>
        <Box sx={{ display: "flex", gap: 2 }}>
          <Box component={NavLink} to="/" end sx={linkSx}>
            Home
          </Box>
          <Box component={NavLink} to="/market" sx={linkSx}>
            Market
          </Box>
        </Box>
      </Box>
      <Box component="main" sx={{ flex: 1 }}>
        <Outlet />
      </Box>
    </Box>
  );
}
