from django.conf import settings

FERIAS = {
    "hyvolution": {
    "nombre": "Hyvolution Chile",
    "url": "https://chile.hyvolution.com/wp-json/leads/v1/get/",
    "token": settings.HYVOLUTION_API_TOKEN,
    "logo": "logos/hyvolution.png",
    "cf7_ids": {
            "es": 2527,
            "en": 3767
        }
    },

    "seguridadexpo": {
        "nombre": "SeguridadExpo",
        "url": "https://seguridadexpo.cl/wp-json/leads/v1/get/",
        "token": settings.SEGURIDAD_API_TOKEN,
        "logo": "logos/seguridadexpo.png",
        "cf7_ids": {
            "es": 9080,
            "en": 9361
        }
    },
    "exponaval": {
        "nombre": "Exponaval",
        "url": "https://exponaval.cl/wp-json/leads/v1/get/",
        "token": settings.EXPONAVAL_API_TOKEN,
        "logo": "logos/exponaval.png",
        "cf7_ids": {
            "es": 10262,
            "en": 10263
        }
    },
    "enloce": {
        "nombre": "Enloce",
        "url": "https://enloce.cl/wp-json/leads/v1/get/",
        "token": settings.ENLOCE_API_TOKEN.strip(),
        "logo": "logos/enloce.png",
        "cf7_ids": {
            "es": 4070,
        }
    },

    "exposalud": {
        "nombre": "Exposalud",
        "url": "https://expo-salud.cl/wp-json/leads/v1/get/",
        "token": settings.EXPOSALUD_API_TOKEN.strip(),
        "logo": "logos/exposalud.png",
        "cf7_ids": {
            "es": 10209,
            "en": 10649
        }
    },

    "expovivienda": {
        "nombre": "Expovivienda",
        "url": "https://expovivienda.cl/wp-json/leads/v1/get/",
        "token": settings.EXPOVIVIENDA_API_TOKEN.strip(),
        "logo": "logos/expovivienda.png",
        "cf7_ids": {
            "es": 3665,
        }
    },

    "aquasur": {
        "nombre": "Aquasur",
        "url": "https://aqua-sur.cl/wp-json/leads/v1/get/",
        "token": settings.AQUASUR_API_TOKEN.strip(),
        "logo": "logos/aquasur.png",
        "cf7_ids": {
            "es": 7580,
            "en": 7583
        }
    },

    "aquasurtech": {
        "nombre": "Aquasurtech",
        "url": "https://aquasurtech.cl/wp-json/leads/v1/get/",
        "token": settings.AQUASURTECH_API_TOKEN.strip(),
        "logo": "logos/aquasurtech.png",
        "cf7_ids": {
            "es": 9252,
            "en": 9270
        }
    },
   
   "transport": {
        "nombre": "Trans-port",
        "url": "https://trans-port.cl/wp-json/leads/v1/get/",
        "token": settings.TRANSPORT_API_TOKEN.strip(),
        "logo": "logos/transport.png",
        "cf7_ids": {
            "es": 6571,
        }
    },


    "expomin": {
        "nombre": "expomin",
        "url": "https://expomin.cl/wp-json/leads/v1/get/",
        "token": settings.EXPOMIN_API_TOKEN.strip(),
        "logo": "logos/expomin.png",
        "cf7_ids": {
            "es": 10858,
            "en": 10859
        }
    },
}
