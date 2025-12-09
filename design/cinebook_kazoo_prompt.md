## Cinebook – Kazoo-ready UI/UX prompt

- **Project**: Cinebook — modern, premium, BookMyShow-style movie booking web app.
- **Brand**: “Cinebook” logo/text top-left on every page.
- **Tone**: modern, friendly, premium entertainment.
- **Palette**: deep navy/dark charcoal background; vibrant tomato/electric orange CTAs; soft gray cards; white/near-white text. Kazoo may refine.
- **Typography**: clean, large sans-serif headings; comfortable body.
- **Accessibility**: WCAG AA contrast; keyboard navigation; ARIA labels on forms, carousels, tabs, seat grid; visible focus states.

### Pages & flows (mockups + prototype)
1. **Register**
   - Fields: Full name, Email, Phone, Password, Confirm password, optional profile picture.
   - Password strength indicator; show/hide; validate email/phone numeric/matching passwords.
   - CTA: “Create account”; link to Login. Success → redirect Login + success toast.
2. **Login**
   - Fields: Email/Phone, Password, “Remember me”, “Forgot password?”.
   - CTA: “Login”. Redirect by role: User → User Dashboard; Admin → Admin Dashboard.
3. **User Dashboard**
   - Hero with “Now Showing” & “Coming Soon” carousels.
   - Search; filters (genre/date/format); sort by popularity.
   - Sections: Recommended, Trending, Nearby Theatres, Your Bookings.
   - Movie card: poster, title, rating, runtime, price, “Book”.
   - Poster or Book → showtime + seat selection flow.
4. **Admin/Theatre Owner Dashboard** (separate)
   - Cards: revenue, bookings, occupancy.
   - Manage theatres/screens: add/edit movies, showtimes, seat layout; view bookings & revenue.
   - Table/list of shows with booked % and “Edit seating”.
   - Control to switch screens/seat maps.
5. **Movie Detail + Showtime Selection**
   - Large poster, synopsis, cast, runtime, rating, trailer preview.
   - Showtimes grouped by theatre + date; each has “Select Seats”.
6. **Seat Selection (critical)**
   - Grid: rows A, B, C, D, E, F… top-to-bottom; seats 1..n left-to-right; aligned per row.
   - Seat types: Regular, Premium, Accessible. Legend with colors + price.
   - States: available, selected, booked/unavailable (greyed), reserved/locked, accessible.
   - Hover: show row/number/price. Click toggles; keyboard navigation across grid; role="grid"/"gridcell" with aria-label="Row A Seat 5, Regular, ₹120"; disabled seats not focusable.
   - Summary panel (right on desktop, bottom on mobile): seat list, type, per-seat price, taxes, total; real-time updates; “Confirm selection” CTA. Limit 1..k seats (configurable).
7. **Booking Summary & Payment**
   - Show movie, theatre, showtime, seats, seat types, per-seat price, fees/taxes, total.
   - Payment options UI (card, UPI, wallet placeholders). No backend needed.
   - Primary CTA: “Confirm booking”.
8. **Booking Confirmation**
   - Success state with check icon, booking ref, seats, showtime, theatre, amount.
   - CTAs: “Download/Print ticket”, “Add to My Bookings”, “Back to Home”.
9. **My Bookings**
   - Cards/list with status badges, seats, showtime, theatre, amount.
   - Actions: view booking, download ticket.
10. **Navigation**
    - Navbar: Cinebook logo (left), search (optional), user avatar (right), role switch for admins, links to Dashboard, My Bookings, Login/Logout.
    - Footer: minimal links, support/contact.

### Global UI/UX
- Spacious cards, rounded corners, soft shadows, subtle hover/press; smooth micro-interactions for buttons, seats, toasts (150–250ms ease).
- Responsive: mobile-first; seat grid scrolls horizontally or compacts on small screens; swipeable carousels.
- Dark & Light mode variants (preferred).

### Components & props (for spec/JSON)
- **Navbar**: { role, avatarUrl, unreadCount, onRoleSwitch }
- **PosterCard**: { title, posterUrl, rating, runtime, price, tags[], ctaLabel }
- **SeatGrid**: { rows: ["A"...], seatsPerRow: n OR explicit map, seatTypes: [{type, price, color}], seats: [{row, num, status, type}] }
- **Legend**: derive from seatTypes/status colors.
- **Filters**: genre/date/format chips, search input.
- **Carousels**: keyboard-accessible, ARIA labels.
- **Toasts**: success/error with icons.

### Accessibility notes
- Seat grid: role="grid"; seats role="button"/"gridcell"; aria-label includes row/number/type/price; focusable states; ESC closes dialogs; Enter/Space activates.
- Focus order: navbar → hero → filters → carousels → content → footer; visible focus rings; WCAG AA contrast.

### Breakpoints
- Mobile 320px, Tablet 768px, Desktop 1440px (mockups for each).

### Data examples
- Seat grid:
  ```
  [
    { "row": "A", "seats": [
      { "num": 1, "status": "booked", "type": "Regular", "price": 120 },
      { "num": 2, "status": "available", "type": "Regular", "price": 120 },
      { "num": 3, "status": "available", "type": "Accessible", "price": 120 }
    ]},
    { "row": "B", "seats": [
      { "num": 1, "status": "available", "type": "Premium", "price": 180 }
    ]}
  ]
  ```
- Movie card:
  ```
  { "title": "Interstellar", "posterUrl": "...", "rating": "8.6", "runtime": "169m", "price": 180, "tags": ["IMAX","Sci-Fi"], "ctaLabel": "Book" }
  ```

### Deliverables (Kazoo should output)
- High-fidelity mockups: Register, Login, User Dashboard, Admin Dashboard, Movie Detail, Showtime list, Seat Selection, Booking Summary, Booking Confirmation.
- Interactive prototype: register → login → dashboard → select movie → choose showtime → choose seats → summary → confirm.
- Responsive variants at 320/768/1440.
- Style guide: colors, fonts, spacing, shadows, radii, icons.
- Component library with annotations + props (JSON/Markdown) for Navbar, PosterCard, Filters, SeatGrid, Legend, Toast, Buttons, Forms.
- Assets: PNG/JPG exports + spec file; optional prototype link.

### Implementation guidance (optional)
- Stack: React + Tailwind (or utility-first) or clean HTML/CSS/JS.
- SeatGrid accepts rows array + seatsPerRow or explicit map; supports Regular/Premium/Accessible; statuses available/selected/booked/reserved/locked.
- Use debounced updates for seat selection; show locked/booked distinctly; optimistic UI allowed.

