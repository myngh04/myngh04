<div align="center">

# Nguyen Gia Huy

**Backend-focused Java Developer**  
Building practical systems with clear domain rules and thoughtful user flows.

`Java 21` · `Spring Boot` · `PostgreSQL` · `Spring Security`

</div>

---

## About

I build backend-first web applications and care about the details behind a reliable product: authentication, transactional flows, inventory consistency, and a user experience that stays simple.

Right now, I’m building **MonoMarket** — a marketplace for game accounts and items. It is a personal project where I am turning real product flows into maintainable Spring Boot code.

## Currently building

### [MonoMarket →](https://github.com/myngh4/monomarket)

A server-rendered marketplace built around game inventory, carts, checkout, and account management.

| Product flow | What I’m working on |
| :-- | :-- |
| **Guest shopping** | Visitors can add items before signing in; their cart is merged into their account after login. |
| **Inventory safety** | Each inventory item is treated as unique stock, with locking during checkout to avoid conflicting purchases. |
| **Order lifecycle** | Checkout reserves available inventory; pending orders can be cancelled and their inventory released. |
| **Account experience** | Profile and order-history flows are built with progressive disclosure rather than unnecessary page jumps. |

## Stack

| Backend | Data & infrastructure | Web |
| :-- | :-- | :-- |
| Java 21 · Spring Boot · Spring MVC | PostgreSQL · JPA/Hibernate · Flyway | Thymeleaf · HTML · CSS · JavaScript |
| Spring Security · Maven | H2 for tests · JSONB | Server-rendered UI |

## How I like to build

- Keep business rules in the service layer, not hidden in the UI.
- Treat database consistency as a product feature.
- Start with a working flow, then refine it through tests and real edge cases.
- Prefer clear, maintainable code over adding abstractions too early.
- Build locally, iterate carefully, and keep the project genuinely mine.

---

<div align="center">

**Open to learning, building, and shipping better systems one feature at a time.**

</div>
