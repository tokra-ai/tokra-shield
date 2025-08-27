import re, unicodedata
SEP_CHARS = r"\.\-_\u2212\u00b7\u2022/\\"
_CONF_MAP = str.maketrans({
  "а":"a","е":"e","о":"o","с":"c","р":"p","у":"y","х":"x","і":"i","ј":"j","ѕ":"s",
  "ӏ":"l","ԁ":"d","ԍ":"g","ԛ":"q","ԝ":"w","ԃ":"d","ѵ":"v"
})
def normalize(s:str, allow_zero_sep:bool=True)->str:
  if not s: return ""
  s = unicodedata.normalize("NFKC", s).casefold()
  out=[]
  for ch in s:
    cat = unicodedata.category(ch)
    if cat.startswith("C"):
      if allow_zero_sep and cat=="Cf":
        out.append(" ")
      # غير ذلك نتجاهله
      continue
    out.append(ch)
  s = "".join(out).translate(_CONF_MAP)
  s = re.sub(f"[\\s{SEP_CHARS}]+", " ", s)
  s = re.sub(r"\s+", " ", s).strip()
  return s
def strip_spaces(s:str)->str:
  return re.sub(r"\s+", "", s or "")
