import express from 'express';

const app = express();
app.use(express.json({ limit: '256kb' }));

const PORT = process.env.PORT || 8080;
const GOOGLE_MAPS_API_KEY = process.env.GOOGLE_MAPS_API_KEY;
const ALLOWED_ORIGIN = process.env.ALLOWED_ORIGIN || 'https://shoheikanaya-wq.github.io';

app.use((req, res, next) => {
  res.setHeader('Access-Control-Allow-Origin', ALLOWED_ORIGIN);
  res.setHeader('Vary', 'Origin');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  res.setHeader('Access-Control-Allow-Methods', 'GET,POST,OPTIONS');
  if (req.method === 'OPTIONS') return res.sendStatus(204);
  next();
});

app.get('/health', (_req, res) => {
  res.json({ ok: true, service: 'tokai-pan-route-api' });
});

function validPoint(p) {
  return p && Number.isFinite(Number(p.lat)) && Number.isFinite(Number(p.lng));
}

function waypoint(p) {
  return { location: { latLng: { latitude: Number(p.lat), longitude: Number(p.lng) } } };
}

app.post('/route', async (req, res) => {
  try {
    if (!GOOGLE_MAPS_API_KEY) {
      return res.status(503).json({ error: 'route_api_not_configured' });
    }

    const { origin, destination, intermediates = [], vehicle = 'car' } = req.body || {};
    if (!validPoint(origin) || !validPoint(destination)) {
      return res.status(400).json({ error: 'invalid_origin_or_destination' });
    }
    if (!Array.isArray(intermediates) || intermediates.length > 23 || intermediates.some(p => !validPoint(p))) {
      return res.status(400).json({ error: 'invalid_intermediates' });
    }

    const travelMode = vehicle === 'bike' ? 'TWO_WHEELER' : 'DRIVE';
    const body = {
      origin: waypoint(origin),
      destination: waypoint(destination),
      intermediates: intermediates.map(waypoint),
      travelMode,
      routingPreference: 'TRAFFIC_AWARE',
      computeAlternativeRoutes: false,
      languageCode: 'ja-JP',
      units: 'METRIC'
    };

    const r = await fetch('https://routes.googleapis.com/directions/v2:computeRoutes', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Goog-Api-Key': GOOGLE_MAPS_API_KEY,
        'X-Goog-FieldMask': 'routes.distanceMeters,routes.duration,routes.staticDuration,routes.legs.distanceMeters,routes.legs.duration,routes.legs.staticDuration'
      },
      body: JSON.stringify(body)
    });

    const text = await r.text();
    if (!r.ok) {
      console.error('Routes API error', r.status, text.slice(0, 1000));
      return res.status(502).json({ error: 'routes_api_failed', status: r.status });
    }

    const data = JSON.parse(text);
    const route = data.routes?.[0];
    if (!route) return res.status(502).json({ error: 'no_route' });

    const seconds = s => Number(String(s || '0s').replace('s', '')) || 0;
    res.json({
      distanceMeters: route.distanceMeters || 0,
      durationSeconds: seconds(route.duration),
      staticDurationSeconds: seconds(route.staticDuration),
      legs: (route.legs || []).map((leg, index) => ({
        index,
        distanceMeters: leg.distanceMeters || 0,
        durationSeconds: seconds(leg.duration),
        staticDurationSeconds: seconds(leg.staticDuration)
      }))
    });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'internal_error' });
  }
});

app.listen(PORT, () => console.log(`route-api listening on ${PORT}`));
