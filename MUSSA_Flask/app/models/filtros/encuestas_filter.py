from app.models.encuestas_models import EncuestaGenerada, GrupoEncuesta


def filtrar_encuestas(filtro):
    query = EncuestaGenerada.query

    if "categorias" in filtro:
        ids_grupo = [GrupoEncuesta.query.filter_by(numero_grupo=categoria).first().id for categoria in
                     filtro["categorias"]]
        query = query.filter(EncuestaGenerada.grupo_id.in_(ids_grupo))

    return query.order_by(EncuestaGenerada.orden.asc()).all()
