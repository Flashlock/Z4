export interface Listing {
  id: number;
  component_id: number | null;
  marketplace: string;
  title: string;
  listing_url: string;
  seller: string;
  condition: string;
  reliability_score: number;
  price_cents: number;
  currency: string;
  image_url: string;
  manufacturer: string | null;
  model: string | null;
  category: string | null;
}

export interface Component {
  id: number;
  category: string;
  manufacturer: string;
  model: string;
}

export interface Goal {
  text: string;
}

export interface MasterSlot {
  category: string;
  component: Component;
  listing: Listing | null;
  locked_at: string;
}

export interface MasterBuild {
  slots: MasterSlot[];
  total_cents: number;
  currency: string;
}

export interface DraftSlot {
  category: string;
  locked: boolean;
  component: Component;
  listing: Listing | null;
}

export interface DraftBuild {
  id: string;
  title: string;
  total_cents: number;
  currency: string;
  slots: DraftSlot[];
}

export interface HomeProjection {
  goal: Goal;
  master: MasterBuild;
  drafts: DraftBuild[];
}

export interface ComponentGroup {
  component: Component;
  listings: Listing[];
}

export interface MarketProjection {
  groups: ComponentGroup[];
}
