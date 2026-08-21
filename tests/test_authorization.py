import pytest
from qualidade_flask import create_app, db
from qualidade_flask.models import User, Empresa, Projeto
from werkzeug.security import generate_password_hash


def make_app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    # Disable CSRF for tests
    app.config['WTF_CSRF_ENABLED'] = False
    return app


def test_user_cannot_create_project_with_other_users_company():
    app = make_app()
    client = app.test_client()

    with app.app_context():
        db.drop_all()
        db.create_all()
        # Create two users
        u_a = User(username='user_a', password=generate_password_hash('passA'))
        u_b = User(username='user_b', password=generate_password_hash('passB'))
        db.session.add_all([u_a, u_b])
        db.session.commit()

        # Create a company for user B
        company_b = Empresa(razao_social='Empresa B', user_id=u_b.id)
        db.session.add(company_b)
        db.session.commit()

        # Login as user A
        resp = client.post('/login', data={'username': 'user_a', 'password': 'passA'}, follow_redirects=True)
        assert resp.status_code == 200

        # Attempt to create a project pointing to company_b
        resp2 = client.post('/projetos/novo', data={'nome': 'ProjX', 'objetivo': 'Obj', 'empresa_id': str(company_b.id)}, follow_redirects=True)
        # Ensure no project was created for user_a with company_b
        proj = Projeto.query.filter_by(user_id=u_a.id, empresa_id=company_b.id).first()
        assert proj is None


def test_user_cannot_delete_other_users_project():
    app = make_app()
    client = app.test_client()

    with app.app_context():
        db.drop_all()
        db.create_all()
        # Create two users
        u_a = User(username='user_a2', password=generate_password_hash('passA2'))
        u_b = User(username='user_b2', password=generate_password_hash('passB2'))
        db.session.add_all([u_a, u_b])
        db.session.commit()

        # Create a project for user B
        # Create project for user B using correct field names
        proj_b = Projeto(nome='ProjB', objetivo='ObjB', user_id=u_b.id)
        db.session.add(proj_b)
        db.session.commit()

        # Login as user A
        resp = client.post('/login', data={'username': u_a.username, 'password': 'passA2'})
        assert resp.status_code in (302, 200)

        # Try to delete project of user B
        resp2 = client.post(f'/projeto/{proj_b.id}/excluir')
        # Should be forbidden: 404 (not found for non-owner) or 403 or redirect
        assert resp2.status_code in (404, 403, 302)
        # Project still exists
        assert Projeto.query.get(proj_b.id) is not None
