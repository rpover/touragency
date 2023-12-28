import uvicorn
import fastapi
from fastapi.responses import RedirectResponse
from src.server.router import routers
from src.server.database.dbmanager import DbManager
import settings

app = fastapi.FastAPI(title='taAPI',
                      version='0.1 Alpha',
                      description='taAPI - TourAgency Application Programming Interface')

[app.include_router(router) for router in routers]


@app.router.get('/', include_in_schema=False)
def index() -> RedirectResponse:
    return RedirectResponse('/docs')


if __name__ == '__main__':
    DbManager(settings.DATABASE_PATH).create_db(f'{settings.SQL_SCRIPTS_DIR}/create.sql')

    if settings.DEBUG:
        try:
            DbManager(settings.DATABASE_PATH).execute_sql_script(f'{settings.SQL_SCRIPTS_DIR}/fill.sql')
        except:
            pass

    uvicorn.run('server:app', reload=True, host=settings.SERVER_HOST, port=settings.SERVER_PORT)
