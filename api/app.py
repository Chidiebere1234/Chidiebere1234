from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from engines.models.model import db
from engines.models.chats import db as chats_db
from engines.models.account import db as account_db
from engines.models.borrower import db as borrow_db
from engines.models.notification import db as notif_db
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import (CORS, cross_origin)
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate



def create_app() -> Flask:
    """
    Create and configure the Flask application.

    Returns:
        Flask: The configured Flask application.
    """
    app = Flask(__name__)


    # CORS Origin Layout For Future Use [To be Implimented later]
    CORS(app, resources={r"/*": {"origins": "*"}})
    # CORS(app, resources={r"/dispute": {"origins": "*"},
    #     r"auth_bp/*": "origins": "["auth/unauthorized", "auth/bad-request", "auth/forbidden"]"
    #     })

    # Database Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://dev_test:DevLog#1@localhost/iwallet_fcmb_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = False

    # Adding JWT Token Configuration
    app.config['SECRET_KEY'] = 'iwallet_fcmb_em3%h2#40i&*Sek@73HDnje9972ep*@&^#@12kdmsf1182'
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access']


    # Migrate App
    migrate = Migrate(app, db)

    # Register All Models [This method of creating databases from multiple files is not working yet
    # model_files = [db, borrow_db, chats_db, account_db, notif_db]
    # db.init_app(app, model_files=model_files)

    # Initialize the database
    db.init_app(app)
    with app.app_context():
        print("Initializing database...")
        db.create_all()
        print("Database initialized.")

    SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
    # API_URL = 'http://petstore.swagger.io/v2/swagger.json'  # Our API url (can of course be a local resource)
    # API_URL = 'http://127.0.0.1:5005/file/iwallet_ui.json'

    # Doc: https://pypi.org/project/flask-swagger-ui/
    # Call factory function to create our blueprint
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
        # API_URL,
        config={  # Swagger UI config overrides
            'app_name': "I Wallet API"
        },
        # oauth_config={  # OAuth config. See https://github.com/swagger-api/swagger-ui#oauth2-configuration .
        #    'clientId': "your-client-id",
        #    'clientSecret': "your-client-secret-if-required",
        #    'realm': "your-realms",
        #    'appName': "your-app-name",
        #    'scopeSeparator': " ",
        #    'additionalQueryStringParams': {'test': "hello"}
        # }
    )


    # Import and register blueprints for each feature
    from .routes.loan import loan_bp
    from .routes.messaging import messaging_bp
    from .routes.feedback import feedback_bp
    from .routes.referral import referral_bp
    from .routes.location import location_bp
    from .routes.authentication import auth_bp
    from .routes.dispute import dispute_bp
    from .routes.review import review_bp
    from .routes.transaction import transaction_bp
    from .routes.chatbot import chatbot_bp
    from .routes.faq import faq_bp
    from .routes.support import support_bp
    from .routes.notifications import notifications_bp

    # Register blueprints
    # Register Swagger Bluprint
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    # Application Blueprints
    app.register_blueprint(loan_bp, url_prefix='/loan')
    app.register_blueprint(messaging_bp, url_prefix='/messaging')
    app.register_blueprint(feedback_bp, url_prefix='/feedback')
    app.register_blueprint(referral_bp, url_prefix='/referral')
    app.register_blueprint(location_bp, url_prefix='/location')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(dispute_bp, url_prefix='/dispute')
    app.register_blueprint(review_bp, url_prefix='/review')
    app.register_blueprint(transaction_bp, url_prefix='/transaction')
    app.register_blueprint(chatbot_bp, url_prefix='/chatbot')
    app.register_blueprint(faq_bp, url_prefix='/faq')
    app.register_blueprint(support_bp, url_prefix='/support')
    app.register_blueprint(notifications_bp, url_prefix='/notifications')


    return app

# app = create_app()
