from src.server.routers import user, country, tour, ticket

routers = (user.router,
           country.router,
           tour.router,
           ticket.router)
