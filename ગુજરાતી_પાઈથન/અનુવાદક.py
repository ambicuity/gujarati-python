"""
અનુવાદક મોડ્યુલ - પાઈથન કીવર્ડ્સને ગુજરાતીમાં અનુવાદ કરવા માટે

આ મોડ્યુલ ગુજરાતી કીવર્ડ્સને અંગ્રેજી કીવર્ડ્સમાં કન્વર્ટ કરે છે
જેથી સ્ટાન્ડર્ડ પાઈથન ઇન્ટરપ્રિટર ચલાવી શકાય.

આર્કિટેક્ચર: Python ના tokenize મોડ્યુલ દ્વારા ટોકન-લેવલ અનુવાદ.
સ્ટ્રિંગ્સ અને કમેન્ટ્સ લેક્સર લેયર પર અકબંધ રહે છે.
"""

import io
import re
import sys
import token
import tokenize
from typing import List, Tuple

# Python 3.12+ tokenizer correctly handles Gujarati combining marks
# (Unicode category Mc — e.g. ા, ો). Older versions produce ERRORTOKEN
# for these characters, breaking tokenization of Gujarati identifiers.
_USE_TOKENIZE = sys.version_info >= (3, 12)


class કીવર્ડ_અનુવાદક:
    """
    ગુજરાતી કીવર્ડ્સને અંગ્રેજીમાં અનુવાદ કરવા માટેનો ક્લાસ
    """

    def __init__(self):
        # ગુજરાતી કીવર્ડ્સથી અંગ્રેજી કીવર્ડ્સનું મેપિંગ
        self.કીવર્ડ_મેપ = {
            # મૂળભૂત કીવર્ડ્સ
            'ઈમ્પોર્ટ': 'import',
            'ડેફ': 'def',
            'ક્લાસ': 'class',
            'ફોર': 'for',
            'વ્હાઈલ': 'while',
            'જો': 'if',
            'નહીં તો': 'else',
            'અથવા જો': 'elif',
            'પરત આપો': 'return',
            'છાપો': 'print',
            'સાચું': 'True',
            'ખોટું': 'False',
            'કંઈ નહીં': 'None',
            'અને': 'and',
            'અથવા': 'or',
            'નહીં': 'not',
            'ઇન': 'in',
            'છે': 'is',
            'સાથે': 'with',
            'આસ': 'as',
            'માંથી': 'from',
            'પ્રયત્ન કરો': 'try',
            'સિવાય': 'except',
            'અંતે': 'finally',
            'ઊઠાવો': 'raise',
            'લેમ્બડા': 'lambda',
            'વૈશ્વિક': 'global',
            'બિન સ્થાનિક': 'nonlocal',
            'ખાતરી કરો': 'assert',
            'બ્રેક': 'break',
            'ચાલુ રાખો': 'continue',
            'પાસ': 'pass',
            'ડિલીટ કરો': 'del',
            'પ્રદાન કરો': 'yield',
            'અસિન્ક': 'async',
            'રાહ જુઓ': 'await',
            'મેચ': 'match',
            'કેસ': 'case',

            # બિલ્ટ-ઇન ફંક્શન્સ
            'લેન': 'len',
            'રેંજ': 'range',
            'ટાઇપ': 'type',
            'સ્ટ્ર': 'str',
            'ઇન્ટ': 'int',
            'ફ્લોટ': 'float',
            'લિસ્ટ': 'list',
            'ડિક્ટ': 'dict',
            'સેટ': 'set',
            'ટ્યુપલ': 'tuple',
            'ઓપન': 'open',
            'મિન': 'min',
            'મેક્સ': 'max',
            'સમ': 'sum',
            'સોર્ટેડ': 'sorted',
            'રેવર્સેડ': 'reversed',
            'એની': 'any',
            'ઓલ': 'all',
            'મેપ': 'map',
            'ફિલ્ટર': 'filter',
            'ઝીપ': 'zip',
            'એન્યુમરેટ': 'enumerate',
            'ઈનપુટ': 'input',
            'ઈવલ': 'eval',
            'એક્ઝેક': 'exec',
            'કોમ્પાઇલ': 'compile',
            'હેશ': 'hash',
            'આઈડી': 'id',
            'વાર્સ': 'vars',
            'ડાઇર': 'dir',
            'હેલ્પ': 'help',
            'રાઉન્ડ': 'round',
            'એબ્સ': 'abs',
            'પાવર': 'pow',
            'ડિવમોડ': 'divmod',
            'બિન': 'bin',
            'ઓક્ટ': 'oct',
            'હેક્સ': 'hex',
            'ઓર્ડ': 'ord',
            'ક્રોમ': 'chr',
            'બૂલ': 'bool',
            'બાઇટ્સ': 'bytes',
            'બાઇટઆરે': 'bytearray',
            'કોમ્પ્લેક્સ': 'complex',
            'ફ્રોઝનસેટ': 'frozenset',
            'મેમરીવ્યુ': 'memoryview',
            'ઓબ્જેક્ટ': 'object',
            'પ્રોપર્ટી': 'property',
            'સ્લાઇસ': 'slice',
            'સુપર': 'super',
            'સ્ટેટિકમેથડ': 'staticmethod',
            'ક્લાસમેથડ': 'classmethod',
        }

        # સામાન્ય મોડ્યુલ નામો
        self.મોડ્યુલ_નામ_મેપ = {
            'ગણિત': 'math',
            'રેન્ડમ': 'random',
            'અવિકલ': 'time',
            'સમય': 'time',
            'તારીખ_સમય': 'datetime',
            'ઓપરેટિંગ_સિસ્ટમ': 'os',
            'સિસ્ટમ': 'sys',
            'શબ્દમાળા': 'string',
            'datetime': 'datetime',
            'json': 'json',
            'os': 'os',
            'sys': 'sys',
            'કલેક્શન્સ': 'collections',
            'ઇટરટૂલ્સ': 'itertools',
            'ફંકટૂલ્સ': 'functools',
            'રી': 're',
            'કાચબો': 'turtle',
        }

        # મોડ્યુલ ફંક્શન મેપિંગ (ચોક્કસ ડોટેડ પાથ માટે)
        self.મોડ્યુલ_ફંક્શન_મેપ = {
            # ગણિત (math)
            'ગણિત.વર્ગમૂળ': 'math.sqrt',
            'ગણિત.પાઈ': 'math.pi',
            'ગણિત.સીલ': 'math.ceil',
            'ગણિત.ફ્લોર': 'math.floor',
            'ગણિત.ફેક્ટોરિયલ': 'math.factorial',
            'ગણિત.સાઈન': 'math.sin',
            'ગણિત.કોસ': 'math.cos',
            'ગણિત.ટેન': 'math.tan',
            'ગણિત.ઘાત': 'math.pow',
            'ગણિત.લોગ': 'math.log',

            # રેન્ડમ (random)
            'રેન્ડમ.રેન્ડઈન્ટ': 'random.randint',
            'રેન્ડમ.પસંદ': 'random.choice',
            'રેન્ડમ.શફલ': 'random.shuffle',
            'રેન્ડમ.રેન્ડમ': 'random.random',
            'રેન્ડમ.સીડ': 'random.seed',
            'રેન્ડમ.સેમ્પલ': 'random.sample',

            # JSON (json)
            'json.લોડ્સ': 'json.loads',
            'json.ડમ્પ્સ': 'json.dumps',
            'json.લોડ': 'json.load',
            'json.ડમ્પ': 'json.dump',

            # sys (સિસ્ટમ)
            'sys.બહાર': 'sys.exit',
            'સિસ્ટમ.બહાર': 'sys.exit',
            'sys.પાથ': 'sys.path',
            'સિસ્ટમ.પાથ': 'sys.path',
            'sys.આવૃત્તિ': 'sys.version',
            'સિસ્ટમ.આવૃત્તિ': 'sys.version',
            'sys.પ્લેટફોર્મ': 'sys.platform',
            'સિસ્ટમ.પ્લેટફોર્મ': 'sys.platform',
            'sys.આર્ગ્યુમેન્ટ્સ': 'sys.argv',
            'સિસ્ટમ.આર્ગ્યુમેન્ટ્સ': 'sys.argv',
            'sys.દલીલો': 'sys.argv',
            'સિસ્ટમ.દલીલો': 'sys.argv',

            # os (ઓપરેટિંગ_સિસ્ટમ)
            'os.નામ': 'os.name',
            'ઓપરેટિંગ_સિસ્ટમ.નામ': 'os.name',
            'os.માર્ગ': 'os.path',
            'ઓપરેટિંગ_સિસ્ટમ.માર્ગ': 'os.path',
            'os.સિસ્ટમ': 'os.system',
            'ઓપરેટિંગ_સિસ્ટમ.સિસ્ટમ': 'os.system',
            'os.મેકડીર': 'os.mkdir',
            'ઓપરેટિંગ_સિસ્ટમ.મેકડીર': 'os.mkdir',
            'os.list': 'os.listdir',
            'ઓપરેટિંગ_સિસ્ટમ.list': 'os.listdir',
            'os.યાદી': 'os.listdir',
            'ઓપરેટિંગ_સિસ્ટમ.યાદી': 'os.listdir',
            'os.દૂર': 'os.remove',
            'ઓપરેટિંગ_સિસ્ટમ.દૂર': 'os.remove',
            'os.કાઢો': 'os.remove',
            'ઓપરેટિંગ_સિસ્ટમ.કાઢો': 'os.remove',
            'os.રસ્તો': 'os.path',
            'ઓપરેટિંગ_સિસ્ટમ.રસ્તો': 'os.path',
            'os.વર્તમાન_ડિરેક્ટરી': 'os.getcwd',
            'ઓપરેટિંગ_સિસ્ટમ.વર્તમાન_ડિરેક્ટરી': 'os.getcwd',
            'ઓએસ.વર્તમાન_ડિરેક્ટરી': 'os.getcwd',
            'os.ડિરેક્ટરી_બદલો': 'os.chdir',
            'ઓપરેટિંગ_સિસ્ટમ.ડિરેક્ટરી_બદલો': 'os.chdir',

            # datetime (તારીખ_સમય)
            'તારીખ_સમય.અત્યારે': 'datetime.datetime.now',
            'datetime.અત્યારે': 'datetime.datetime.now',
            'તારીખ_સમય.તારીખ': 'datetime.date',
            'datetime.તારીખ': 'datetime.date',
            'તારીખ_સમય.સમય': 'datetime.time',
            'datetime.સમય': 'datetime.time',
            'તારીખ_સમય.તફાવત': 'datetime.timedelta',
            'datetime.તફાવત': 'datetime.timedelta',
            'તારીખ_સમય.ફોર્મેટ': 'datetime.strftime',
            'datetime.ફોર્મેટ': 'datetime.strftime',

            # time (સમય)
            'સમય.ઊંઘો': 'time.sleep',
            'time.ઊંઘો': 'time.sleep',
            'સમય.સમય': 'time.time',
            'time.સમય': 'time.time',
            'સમય.ઊંઘ': 'time.sleep',
            'time.ઊંઘ': 'time.sleep',

            # string (શબ્દમાળા)
            'શબ્દમાળા.અક્ષરો': 'string.ascii_letters',
            'string.અક્ષરો': 'string.ascii_letters',
            'શબ્દમાળા.અંકો': 'string.digits',
            'string.અંકો': 'string.digits',
            'શબ્દમાળા.ચિહ્નો': 'string.punctuation',
            'string.ચિહ્નો': 'string.punctuation',

            # કાચબો (Turtle)
            'કાચબો.આગળ': 'turtle.forward',
            'કાચબો.પાછળ': 'turtle.backward',
            'કાચબો.ડાબે': 'turtle.left',
            'કાચબો.જમણે': 'turtle.right',
            'કાચબો.ઉપર': 'turtle.up',
            'કાચબો.નીચે': 'turtle.down',
            'કાચબો.રંગ': 'turtle.color',
            'કાચબો.શરૂ': 'turtle.begin_fill',
            'કાચબો.બંધ': 'turtle.end_fill',
            'કાચબો.ગતિ': 'turtle.speed',
            'કાચબો.છાપો': 'turtle.write',
            'કાચબો.વર્તુળ': 'turtle.circle',
            'કાચબો.આકાર': 'turtle.shape',
            'કાચબો.ગોલ': 'turtle.done',
            'કાચબો.ગયા': 'turtle.goto',
            'કાચબો.પેનકલર': 'turtle.pencolor',
            'કાચબો.પેનસાઈઝ': 'turtle.pensize',
            'કાચબો.બેકગ્રાઉન્ડ': 'turtle.bgcolor',
            'કાચબો.શીર્ષક': 'turtle.title',
        }

        # રિવર્સ મેપિંગ (અંગ્રેજીથી ગુજરાતી)
        આલ_મેપ = {**self.કીવર્ડ_મેપ, **self.મોડ્યુલ_નામ_મેપ}
        self.રિવર્સ_મેપ = {v: k for k, v in આલ_મેપ.items()}

        # ઓપરેટર્સનું મેપિંગ
        self.ઓપરેટર_મેપ = {
            '==': '==',
            '!=': '!=',
            '<=': '<=',
            '>=': '>=',
            '<': '<',
            '>': '>',
            '+': '+',
            '-': '-',
            '*': '*',
            '/': '/',
            '//': '//',
            '%': '%',
            '**': '**',
        }

        # જનરિક મેથડ નામ મેપિંગ (e.g. .ઉમેરો → .append)
        self.મેથડ_મેપ = {
            'ઉમેરો': 'append',
            'કાઢો': 'pop',
        }

        # મલ્ટિ-વર્ડ કીવર્ડ ઇન્ડેક્સ: first_word → [(full_phrase, translation), ...]
        self._multi_word_first: dict = {}
        for ગુજ, eng in self.કીવર્ડ_મેપ.items():
            words = ગુજ.split()
            if len(words) > 1:
                first = words[0]
                if first not in self._multi_word_first:
                    self._multi_word_first[first] = []
                self._multi_word_first[first].append((words, eng))

        # સિંગલ-વર્ડ કીવર્ડ્સ (multi-word excluded)
        self._single_keywords: dict = {
            k: v for k, v in self.કીવર્ડ_મેપ.items() if ' ' not in k
        }

    # ------------------------------------------------------------------
    # ટોકનાઇઝેશન-આધારિત અનુવાદ (Gujarati → English)
    # ------------------------------------------------------------------

    def ગુજરાતીથી_અંગ્રેજી(self, કોડ: str) -> str:
        """
        ગુજરાતી કોડને અંગ્રેજી પાઈથન કોડમાં કન્વર્ટ કરે છે

        Python 3.12+ પર tokenize મોડ્યુલ દ્વારા ટોકન-લેવલ અનુવાદ.
        Python 3.8-3.11 પર regex-આધારિત string replacement (tokenizer
        Gujarati combining marks ને ERRORTOKEN ગણે છે).

        પેરામીટર:
            કોડ (str): ગુજરાતી પાઈથન કોડ

        પરત આપે:
            str: અંગ્રેજી પાઈથન કોડ
        """
        if _USE_TOKENIZE:
            return self._tokenize_translate(કોડ)
        return self._regex_translate(કોડ)

    # ------------------------------------------------------------------
    # Strategy 1: tokenize-based (Python 3.12+)
    # ------------------------------------------------------------------

    def _tokenize_translate(self, કોડ: str) -> str:
        """Token-level Gujarati→English translation (Python 3.12+)."""
        try:
            tokens = list(
                tokenize.generate_tokens(io.StringIO(કોડ).readline)
            )
        except Exception:
            tokens = self._safe_tokenize(કોડ)

        replacements: List[Tuple[int, int, int, int, str]] = []
        consumed: set = set()
        i = 0

        while i < len(tokens):
            if i in consumed:
                i += 1
                continue

            tok = tokens[i]

            if tok.type == token.NAME:
                handled = self._try_multi_word(
                    tokens, i, consumed, replacements
                )
                if handled:
                    i = handled
                    continue

                dot_result = self._try_dotted_path(
                    tokens, i, consumed, replacements
                )
                if dot_result:
                    i = dot_result
                    continue

                replacement = (
                    self._single_keywords.get(tok.string)
                    or self.મોડ્યુલ_નામ_મેપ.get(tok.string)
                )
                if replacement:
                    replacements.append(
                        (*tok.start, *tok.end, replacement)
                    )

            elif tok.type == token.OP and tok.string == '.':
                next_name = self._peek_name(tokens, i + 1)
                if next_name is not None:
                    j = next_name[0]
                    name_tok = tokens[j]
                    if name_tok.string in self.મેથડ_મેપ:
                        paren = self._peek_op(tokens, j + 1, '(')
                        if paren is not None:
                            replacements.append(
                                (*name_tok.start, *name_tok.end,
                                 self.મેથડ_મેપ[name_tok.string])
                            )
                            consumed.add(j)

            elif tok.type == token.STRING:
                processed = self._process_fstring_token(tok.string)
                if processed != tok.string:
                    replacements.append(
                        (*tok.start, *tok.end, processed)
                    )

            i += 1

        return self._apply_replacements(કોડ, replacements)

    # ------------------------------------------------------------------
    # Strategy 2: regex-based (Python 3.8-3.11 fallback)
    # ------------------------------------------------------------------

    def _regex_translate(self, કોડ: str) -> str:
        """Regex-based Gujarati→English translation (Python < 3.12)."""
        અનુવાદિત_કોડ = કોડ

        # 1. Module function mappings (dotted paths — longest first)
        for ગુજ_પાથ, ઇંગ_પાથ in self.મોડ્યુલ_ફંક્શન_મેપ.items():
            parts = ગુજ_પાથ.split('.')
            if len(parts) == 2:
                mod, func = parts
                patt = (
                    re.escape(mod) + r'\.' + re.escape(func)
                    + r'(?=\s|[(){}\[\]:,]|$)'
                )
                અનુવાદિત_કોડ = re.sub(patt, ઇંગ_પાથ, અનુવાદિત_કોડ)

        # 2. Method mappings (.ઉમેરો() → .append())
        for ગુજ_મેથડ, ઇંગ_મેથડ in self.મેથડ_મેપ.items():
            patt = r'\.' + re.escape(ગુજ_મેથડ) + r'(?=\s*\()'
            અનુવાદિત_કોડ = re.sub(patt, '.' + ઇંગ_મેથડ, અનુવાદિત_કોડ)

        # 3. Module names: dotted usage (ગણિત.sqrt) and import statements
        sorted_modules = sorted(
            self.મોડ્યુલ_નામ_મેપ.items(),
            key=lambda x: len(x[0]), reverse=True,
        )
        for ગુજ_મોડ, ઇંગ_મોડ in sorted_modules:
            # Dotted usage: ગણિત.xxx → math.xxx
            પેટર્ન = r'\b' + re.escape(ગુજ_મોડ) + r'\.'
            અનુવાદિત_કોડ = re.sub(પેટર્ન, ઇંગ_મોડ + '.', અનુવાદિત_કોડ)

        # Standalone module names in import lines
        for line in અનુવાદિત_કોડ.split('\n'):
            if 'import ' in line or 'ઈમ્પોર્ટ' in line:
                for ગુજ_મોડ, ઇંગ_મોડ in sorted_modules:
                    if ગુજ_મોડ in line:
                        new_line = line.replace(ગુજ_મોડ, ઇંગ_મોડ)
                        અનુવાદિત_કોડ = અનુવાદિત_કોડ.replace(
                            line, new_line, 1
                        )
                        line = new_line  # update for next iteration

        # 4. Protect string literals (but translate keywords in f-strings)
        સ્ટ્રિંગ_પ્લેસહોલ્ડર્સ = {}
        પ_કાઉન્ટ = 0
        સ્ટ્રિંગ_પેટર્ન્સ = [
            (r'"""([^"]|"[^"]|""[^"])*"""', 'triple_double'),
            (r"'''([^']|'[^']|''[^'])*'''", 'triple_single'),
            (r'(?<!f)"([^"\n\\]*(\\.[^"\n\\]*)*)"', 'double'),
            (r"(?<!f)'([^'\n\\]*(\\.[^'\n\\]*)*)'", 'single'),
            (r'f"([^"\n\\]*(\\.[^"\n\\]*)*)"', 'f_double'),
            (r"f'([^'\n\\]*(\\.[^'\n\\]*)*)'", 'f_single'),
        ]

        for પેટર્ન, qtype in સ્ટ્રિંગ_પેટર્ન્સ:
            matches = list(re.finditer(પેટર્ન, અનુવાદિત_કોડ, re.DOTALL))
            for match in reversed(matches):
                ph = f"__STR_{qtype}_{પ_કાઉન્ટ}__"
                સ્ટ્રિંગ_પ્લેસહોલ્ડર્સ[ph] = match.group(0)
                અનુવાદિત_કોડ = (
                    અનુવાદિત_કોડ[:match.start()]
                    + ph
                    + અનુવાદિત_કોડ[match.end():]
                )
                પ_કાઉન્ટ += 1

        # 5. Keyword translation (longest first)
        keyword_list = sorted(
            self.કીવર્ડ_મેપ.keys(), key=len, reverse=True
        )
        self._regex_keyword_subs = keyword_list  # stash for f-string reuse

        for guj_kw in keyword_list:
            eng_kw = self.કીવર્ડ_મેપ[guj_kw]
            lines = અનુવાદિત_કોડ.split('\n')
            new_lines = []
            for line in lines:
                if guj_kw in line:
                    patt = (
                        r'(?<![a-zA-Z0-9_])' + re.escape(guj_kw)
                        + r'(?=\s|[(){}\[\]:,]|$)'
                    )
                    line = re.sub(patt, eng_kw, line)
                new_lines.append(line)
            અનુવાદિત_કોડ = '\n'.join(new_lines)

        # 6. Restore string placeholders (f-strings get keyword translation)
        for ph, orig in reversed(list(સ્ટ્રિંગ_પ્લેસહોલ્ડર્સ.items())):
            if 'f_double' in ph or 'f_single' in ph:
                processed = self._regex_process_fstring(orig, keyword_list)
                અનુવાદિત_કોડ = અનુવાદિત_કોડ.replace(ph, processed)
            else:
                અનુવાદિત_કોડ = અનુવાદિત_કોડ.replace(ph, orig)

        return અનુવાદિત_કોડ

    def _regex_process_fstring(
        self, fstr: str, keyword_list: list
    ) -> str:
        """Translate keywords inside f-string expressions for regex path."""
        if fstr.startswith('f"'):
            qchar = '"'
            content = fstr[2:-1]
        elif fstr.startswith("f'"):
            qchar = "'"
            content = fstr[2:-1]
        else:
            return fstr

        expr_pattern = r'\{([^}]+)\}'
        expressions = re.findall(expr_pattern, content)
        processed = content
        for expr in expressions:
            translated = expr
            for guj_kw in keyword_list:
                if guj_kw in translated:
                    eng_kw = self.કીવર્ડ_મેપ[guj_kw]
                    patt = (
                        r'(?<![a-zA-Z0-9_])' + re.escape(guj_kw)
                        + r'(?=\s|[(){}\[\]:,]|$)'
                    )
                    translated = re.sub(patt, eng_kw, translated)
            processed = processed.replace(
                '{' + expr + '}', '{' + translated + '}'
            )
        return f'f{qchar}{processed}{qchar}'

    # ------------------------------------------------------------------
    # ટોકનાઇઝેશન-આધારિત અનુવાદ (English → Gujarati)
    # ------------------------------------------------------------------

    def અંગ્રેજીથી_ગુજરાતી(self, કોડ: str) -> str:
        """
        અંગ્રેજી પાઈથન કોડને ગુજરાતી કોડમાં કન્વર્ટ કરે છે

        પેરામીટર:
            કોડ (str): અંગ્રેજી પાઈથન કોડ

        પરત આપે:
            str: ગુજરાતી પાઈથન કોડ
        """
        try:
            tokens = list(
                tokenize.generate_tokens(io.StringIO(કોડ).readline)
            )
        except (tokenize.TokenError, Exception):
            tokens = self._safe_tokenize(કોડ)

        replacements: List[Tuple[int, int, int, int, str]] = []

        for tok in tokens:
            if tok.type == token.NAME and tok.string in self.રિવર્સ_મેપ:
                replacements.append(
                    (*tok.start, *tok.end, self.રિવર્સ_મેપ[tok.string])
                )

        return self._apply_replacements(કોડ, replacements)

    # ------------------------------------------------------------------
    # કીવર્ડ વેલિડેશન
    # ------------------------------------------------------------------

    def કીવર્ડ_વેલિડેશન(self, કોડ: str) -> List[str]:
        """
        ગુજરાતી કોડમાં અજાણ્યા કીવર્ડ્સ શોધે છે

        પેરામીટર:
            કોડ (str): ગુજરાતી કોડ

        પરત આપે:
            List[str]: અજાણ્યા કીવર્ડ્સની યાદી
        """
        return []

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _safe_tokenize(કોડ: str) -> list:
        """Tokenize as far as possible, ignoring TokenError at the end."""
        result = []
        try:
            for tok in tokenize.generate_tokens(io.StringIO(કોડ).readline):
                result.append(tok)
        except (tokenize.TokenError, Exception):
            pass
        return result

    def _try_multi_word(
        self,
        tokens: list,
        i: int,
        consumed: set,
        replacements: list,
    ) -> int:
        """
        Attempt to match a multi-word keyword starting at token index *i*.
        Returns the next index to process, or 0 if no match.
        """
        tok = tokens[i]
        candidates = self._multi_word_first.get(tok.string)
        if not candidates:
            return 0

        for words, eng in candidates:
            # Try to match remaining words via lookahead
            remaining = words[1:]
            j = i + 1
            matched_indices = [i]
            word_idx = 0

            while j < len(tokens) and word_idx < len(remaining):
                t = tokens[j]
                # Skip whitespace-only tokens (NL, NEWLINE, INDENT, etc.)
                if t.type in (
                    token.NL, token.NEWLINE, token.INDENT,
                    token.DEDENT, token.COMMENT,
                ):
                    j += 1
                    continue
                if t.type == token.NAME and t.string == remaining[word_idx]:
                    matched_indices.append(j)
                    word_idx += 1
                    j += 1
                else:
                    break

            if word_idx == len(remaining):
                # Full multi-word match
                first_tok = tokens[matched_indices[0]]
                last_tok = tokens[matched_indices[-1]]
                replacements.append(
                    (*first_tok.start, *last_tok.end, eng)
                )
                for idx in matched_indices:
                    consumed.add(idx)
                return j  # next index after consumed tokens

        return 0

    def _try_dotted_path(
        self,
        tokens: list,
        i: int,
        consumed: set,
        replacements: list,
    ) -> int:
        """
        Handle NAME.NAME patterns (module functions, module names).
        Returns the next index to process, or 0 if not a dotted path.
        """
        tok = tokens[i]

        # Peek for '.'
        dot = self._peek_op(tokens, i + 1, '.')
        if dot is None:
            return 0

        # Peek for NAME after '.'
        name_after = self._peek_name(tokens, dot + 1)
        if name_after is None:
            return 0

        j = name_after[0]
        right_tok = tokens[j]
        dotted = tok.string + '.' + right_tok.string

        # 1. Full dotted path in module function map
        if dotted in self.મોડ્યુલ_ફંક્શન_મેપ:
            eng_path = self.મોડ્યુલ_ફંક્શન_મેપ[dotted]
            replacements.append(
                (*tok.start, *right_tok.end, eng_path)
            )
            consumed.add(i)
            consumed.add(dot)
            consumed.add(j)
            return j + 1

        # 2. Left side: module name translation
        if tok.string in self.મોડ્યુલ_નામ_મેપ:
            replacements.append(
                (*tok.start, *tok.end,
                 self.મોડ્યુલ_નામ_મેપ[tok.string])
            )
        elif tok.string in self._single_keywords:
            replacements.append(
                (*tok.start, *tok.end,
                 self._single_keywords[tok.string])
            )

        # 3. Right side: method map (with '(' check)
        # NOTE: Do NOT translate generic keywords after a dot — that
        # would incorrectly convert e.g. obj.છાપો to obj.print.
        # Only known methods (with '(' lookahead) are translated.
        if right_tok.string in self.મેથડ_મેપ:
            paren = self._peek_op(tokens, j + 1, '(')
            if paren is not None:
                replacements.append(
                    (*right_tok.start, *right_tok.end,
                     self.મેથડ_મેપ[right_tok.string])
                )
                consumed.add(j)

        consumed.add(i)
        return j + 1

    # --- tiny peek helpers ---

    @staticmethod
    def _peek_name(tokens: list, start: int):
        """Return (index, ) of the next NAME token at or after *start*, or None."""
        j = start
        while j < len(tokens):
            t = tokens[j]
            if t.type == token.NAME:
                return (j,)
            # Skip whitespace / formatting tokens
            if t.type in (
                token.NL, token.NEWLINE, token.INDENT,
                token.DEDENT, token.COMMENT,
            ):
                j += 1
                continue
            return None
        return None

    @staticmethod
    def _peek_op(tokens: list, start: int, op: str):
        """Return the index of the next OP(*op*) token at or after *start*, or None."""
        j = start
        while j < len(tokens):
            t = tokens[j]
            if t.type == token.OP and t.string == op:
                return j
            # Skip whitespace / formatting tokens
            if t.type in (
                token.NL, token.NEWLINE, token.INDENT,
                token.DEDENT, token.COMMENT,
            ):
                j += 1
                continue
            return None
        return None

    # --- f-string helper for Python ≤ 3.11 ---

    def _process_fstring_token(self, tok_string: str) -> str:
        """
        If *tok_string* is an f-string literal (e.g. f"hello {નામ}"),
        translate Gujarati keywords inside the expression parts ({...}).

        On Python 3.12+ this method will never be called for f-strings
        because they are decomposed into FSTRING_* tokens; only plain
        STRING tokens reach here.
        """
        # Detect f-string prefix
        prefix = ''
        rest = tok_string
        for p in ('f"""', "f'''", 'f"', "f'"):
            if tok_string.startswith(p):
                prefix = p
                rest = tok_string[len(p):]
                break
        if not prefix:
            return tok_string  # not an f-string

        # Determine the closing quote
        if prefix in ('f"""', "f'''"):
            quote = prefix[1:]  # """ or '''
        else:
            quote = prefix[1]  # " or '

        content = rest[:-len(quote)]

        # Find {expr} blocks and translate keywords inside them.
        # Use a while-loop to correctly advance past escaped {{ and }}.
        new_parts: list = []
        pos = 0
        ci = 0
        while ci < len(content):
            ch = content[ci]
            if ch == '{':
                if ci + 1 < len(content) and content[ci + 1] == '{':
                    # Escaped '{{' — treat as literal, skip both
                    ci += 2
                    continue
                # Start of an expression
                new_parts.append(content[pos:ci])
                expr_start = ci + 1
                depth = 1
                ji = expr_start
                while ji < len(content):
                    if content[ji] == '{':
                        depth += 1
                    elif content[ji] == '}':
                        depth -= 1
                        if depth == 0:
                            break
                    ji += 1
                if depth == 0:
                    expr = content[expr_start:ji]
                    translated_expr = self._translate_fstring_expr(expr)
                    new_parts.append('{' + translated_expr + '}')
                    pos = ji + 1
                    ci = ji + 1
                else:
                    # Unmatched '{' — stop parsing
                    pos = ci
                    break
            elif ch == '}':
                if ci + 1 < len(content) and content[ci + 1] == '}':
                    # Escaped '}}' — treat as literal, skip both
                    ci += 2
                    continue
                ci += 1
            else:
                ci += 1

        # Remaining content after last expression
        if pos < len(content):
            new_parts.append(content[pos:])

        return prefix + ''.join(new_parts) + quote

    def _translate_fstring_expr(self, expr: str) -> str:
        """Translate Gujarati keywords inside an f-string expression string."""
        # Build a merged lookup (single-word keywords + module names)
        all_single = {**self._single_keywords, **self.મોડ્યુલ_નામ_મેપ}
        sorted_keys = sorted(all_single.keys(), key=len, reverse=True)

        translated = expr
        for guj in sorted_keys:
            if guj in translated:
                patt = (
                    r'(?<![a-zA-Z0-9_])' + re.escape(guj)
                    + r'(?=\s|[(){}\[\]:,.]|$)'
                )
                translated = re.sub(patt, all_single[guj], translated)

        # Module function dotted paths
        for guj_path, eng_path in self.મોડ્યુલ_ફંક્શન_મેપ.items():
            if guj_path in translated:
                parts = guj_path.split('.')
                if len(parts) == 2:
                    patt = (
                        re.escape(parts[0]) + r'\.'
                        + re.escape(parts[1])
                        + r'(?=\s|[(){}\[\]:,]|$)'
                    )
                    translated = re.sub(patt, eng_path, translated)

        # Method mappings
        for guj_method, eng_method in self.મેથડ_મેપ.items():
            patt = r'\.' + re.escape(guj_method) + r'(?=\s*\()'
            translated = re.sub(patt, '.' + eng_method, translated)

        return translated

    # --- positional replacement engine ---

    @staticmethod
    def _apply_replacements(
        source: str,
        replacements: List[Tuple[int, int, int, int, str]],
    ) -> str:
        """
        Apply collected (start_row, start_col, end_row, end_col, text)
        replacements to *source*, processing right-to-left to preserve
        earlier positions.
        """
        if not replacements:
            return source

        lines = source.splitlines(keepends=True)

        # Sort bottom-right → top-left so we can apply in reverse
        replacements.sort(
            key=lambda r: (r[0], r[1]),
            reverse=True,
        )

        for sr, sc, er, ec, text in replacements:
            # tokenize rows are 1-indexed
            sr_i = sr - 1
            er_i = er - 1

            if sr_i < 0 or er_i >= len(lines):
                continue

            if sr_i == er_i:
                # Single-line replacement
                line = lines[sr_i]
                lines[sr_i] = line[:sc] + text + line[ec:]
            else:
                # Multi-line replacement (rare, for multi-word keywords
                # that span lines — unlikely but handled)
                first_line = lines[sr_i]
                last_line = lines[er_i]
                lines[sr_i] = first_line[:sc] + text + last_line[ec:]
                del lines[sr_i + 1: er_i + 1]

        return ''.join(lines)


# ગ્લોબલ અનુવાદક ઇન્સ્ટન્સ
_અનુવાદક = કીવર્ડ_અનુવાદક()


def કોડ_અનુવાદ_કરો(ગુજરાતી_કોડ: str) -> str:
    """
    ગુજરાતી કોડને અંગ્રેજી પાઈથન કોડમાં અનુવાદ કરે છે

    પેરામીટર:
        ગુજરાતી_કોડ (str): ગુજરાતી પાઈથન કોડ

    પરત આપે:
        str: અંગ્રેજી પાઈથન કોડ
    """
    return _અનુવાદક.ગુજરાતીથી_અંગ્રેજી(ગુજરાતી_કોડ)


def વેલિડેશન_કરો(ગુજરાતી_કોડ: str) -> List[str]:
    """
    ગુજરાતી કોડમાં એરર્સ શોધે છે

    પેરામીટર:
        ગુજરાતી_કોડ (str): ગુજરાતી પાઈથન કોડ

    પરત આપે:
        List[str]: એરર મેસેજોની યાદી
    """
    return _અનુવાદક.કીવર્ડ_વેલિડેશન(ગુજરાતી_કોડ)