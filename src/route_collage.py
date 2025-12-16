import json
import polyline

class RouteCollage:
    def __init__(self):
        with open('data/2025_activities.json', 'r') as f:
            self.activities = json.load(f)

    def decode_polyline(self, encoded):
        """Decode a polyline string into list of coordinates"""
        if not encoded:
            return []
        return polyline.decode(encoded)

    def normalize_coordinates(self, coords):
        """Normalize coordinates to fit in a small box (0-1 range)"""
        if not coords:
            return []

        lats = [c[0] for c in coords]
        lngs = [c[1] for c in coords]

        min_lat, max_lat = min(lats), max(lats)
        min_lng, max_lng = min(lngs), max(lngs)

        # Avoid division by zero
        lat_range = max_lat - min_lat if max_lat != min_lat else 1
        lng_range = max_lng - min_lng if max_lng != min_lng else 1

        normalized = []
        for lat, lng in coords:
            norm_x = (lng - min_lng) / lng_range
            norm_y = (lat - min_lat) / lat_range
            normalized.append((norm_x, 1 - norm_y))  # Invert Y for SVG

        return normalized

    def create_route_svg_path(self, coords, box_size=200, margin=10):
        """Create SVG path from normalized coordinates"""
        if not coords:
            return ""

        # Scale to box size
        inner_size = box_size - 2 * margin
        scaled = [(x * inner_size + margin, y * inner_size + margin) for x, y in coords]

        # Create path
        path_data = f"M {scaled[0][0]},{scaled[0][1]}"
        for x, y in scaled[1:]:
            path_data += f" L {x},{y}"

        return path_data

    def create_collage(self, routes_per_row=5, box_size=200, padding=20):
        """Create a collage of all route maps"""
        # Get only runs with polylines
        runs = [a for a in self.activities if a['type'] == 'Run' and a.get('map', {}).get('summary_polyline')]

        if not runs:
            return "No routes found"

        # Calculate grid dimensions
        num_routes = len(runs)
        num_rows = (num_routes + routes_per_row - 1) // routes_per_row

        svg_width = routes_per_row * (box_size + padding) + padding
        svg_height = num_rows * (box_size + padding) + padding + 100  # Extra for title

        svg = f'''<svg width="{svg_width}" height="{svg_height}" xmlns="http://www.w3.org/2000/svg">
  <!-- Routes -->
'''

        for idx, run in enumerate(runs):
            row = idx // routes_per_row
            col = idx % routes_per_row

            x = col * (box_size + padding) + padding
            y = row * (box_size + padding) + padding + 100

            # Decode and normalize polyline
            encoded = run['map']['summary_polyline']
            coords = self.decode_polyline(encoded)
            norm_coords = self.normalize_coordinates(coords)
            path_data = self.create_route_svg_path(norm_coords, box_size)

            if path_data:
                # Route path
                svg += f'  <path d="{path_data}" transform="translate({x}, {y})" stroke="#FC4C02" stroke-width="3" fill="none" opacity="0.9"/>\n'

        svg += '</svg>'

        with open('data/route_collage.svg', 'w') as f:
            f.write(svg)

        return svg

if __name__ == "__main__":
    collage = RouteCollage()

    # Generate 5-column version (original)
    collage.create_collage(routes_per_row=5, box_size=180)
    print("Generated route collage (5 columns)!")

    # Generate 6-column version
    svg = collage.create_collage(routes_per_row=6, box_size=150)
    with open('data/route_collage_6col.svg', 'w') as f:
        f.write(svg)
    print("Generated route collage (6 columns)!")

    # Generate 7-column version
    svg = collage.create_collage(routes_per_row=7, box_size=130)
    with open('data/route_collage_7col.svg', 'w') as f:
        f.write(svg)
    print("Generated route collage (7 columns)!")
