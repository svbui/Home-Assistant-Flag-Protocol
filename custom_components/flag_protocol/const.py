DOMAIN = "flag_protocol"

from .flag_rules import nl as country_nl
from .flag_rules import be as country_be
from .flag_rules import se as country_se
from .flag_rules import dk as country_dk
from .flag_rules import no as country_no
from .flag_rules import fi as country_fi
from .flag_rules import is_ as country_is

COUNTRIES = {
    "be": "Belgium",
    "dk": "Denmark",
    "fi": "Finland",
    "is": "Iceland",
    "nl": "Netherlands",
    "no": "Norway",
    "se": "Sweden",
}
COUNTRY_MODULES = {
    "nl": country_nl,
    "be": country_be,
    "se": country_se,
    "dk": country_dk,
    "no": country_no,
    "fi": country_fi,
    "is": country_is,
}
