export const shoots = [
  {
    id: "shoot-1",
    name: "Golden Gate Fog",
    location: "San Francisco, CA",
    capturedAt: "2024-05-01T06:00:00Z",
    tags: ["fog", "bridge", "sunrise"],
  },
  {
    id: "shoot-2",
    name: "Night City",
    location: "Tokyo",
    capturedAt: "2024-04-18T20:00:00Z",
    tags: ["night", "city"],
  },
];

export const photos = [
  { id: "photo-1", shootId: "shoot-1", filename: "DSC0001.RAW", rating: 4 },
  { id: "photo-2", shootId: "shoot-1", filename: "DSC0002.RAW", rating: 3 },
  { id: "photo-3", shootId: "shoot-2", filename: "DSC1001.RAW", rating: 5 },
];

export const timelapses = [
  { id: "tl-1", title: "Fog Rolling In", frameCount: 240 },
];
