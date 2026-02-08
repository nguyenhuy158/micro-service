# Frontend Implementation Plan

## 1. Tech Stack
- **Framework:** Next.js 14+ (App Router)
- **Language:** TypeScript
- **Styling:** Tailwind CSS + shadcn/ui (Radix UI)
- **State Management:** Zustand (lightweight) or React Query (server state)
- **Authentication:** NextAuth.js (integrating with User Service JWT)
- **Deployment:** Docker (for consistency with backend)

## 2. Project Structure
```
frontend/
├── app/
│   ├── (auth)/          # Login/Register routes
│   ├── (dashboard)/     # Main app routes
│   │   ├── products/
│   │   ├── cart/
│   │   └── orders/
│   ├── api/             # BFF (Backend for Frontend) or direct proxy
│   └── layout.tsx
├── components/
│   ├── ui/             # shadcn/ui components
│   ├── forms/          # Reusable forms
│   └── layout/         # Header, Sidebar, Footer
├── lib/
│   ├── api.ts          # Axios/Fetch wrapper pointing to Kong Gateway
│   └── types.ts        # Shared TS interfaces (mirrored from Pydantic)
├── store/              # Zustand stores (e.g. useCartStore)
├── public/
└── Dockerfile
```

## 3. Integration Strategy
- **Gateway Connection:** The Frontend will talk *exclusively* to the Kong Gateway (`http://localhost:8000/api/v1/...`).
- **CORS:** Kong is already configured to allow CORS from `*`.
- **SSR vs Client:**
    - **Public Pages (Products):** Server-Side Rendering (SSR) fetching from Product Service.
    - **Private Pages (Cart, Profile):** Client-Side Rendering (CSR) with `useEffect` or React Query, using the JWT token stored in cookies/localStorage.

## 4. Key Features MVP
1.  **Auth:** Login/Register (calls `POST /api/v1/user/auth/...`).
2.  **Product Catalog:** Grid view of products with search (calls `GET /api/v1/product/products`).
3.  **Shopping Cart:**
    - Local optimistic UI.
    - Sync with `POST /api/v1/order/cart` (if implemented server-side) or just local storage until checkout.
4.  **Checkout:** Simple form to trigger `POST /api/v1/order/orders`.
5.  **Order History:** List of past orders.

## 5. Development Workflow
1.  **Setup:** `npx create-next-app@latest frontend --typescript --tailwind --eslint`.
2.  **Docker:** Add `frontend` service to `docker-compose.yml`.
3.  **Codegen:** Consider using `openapi-typescript-codegen` to generate TS clients from the Unified OpenAPI JSON (`http://localhost:8000/api/docs/openapi.json`).

## 6. Next Steps
- Initialize the Next.js project.
- Configure `docker-compose.yml` to include the frontend.
- Generate API client from the unified Swagger spec.
