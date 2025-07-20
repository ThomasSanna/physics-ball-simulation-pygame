import random
import colorsys

class Colors:
  
  seed = random.randint(0, 1000000)
  functionChosen = None
  
  @staticmethod
  def random_rgb(min_value=0, max_value=255):
    """Génère une couleur RGB aléatoire en utilisant colorsys."""
    h = random.random()
    s = random.uniform(0.5, 1.0)
    v = random.uniform(0.5, 1.0)
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    return (
      int(r * (max_value - min_value) + min_value),
      int(g * (max_value - min_value) + min_value),
      int(b * (max_value - min_value) + min_value)
    )

  @staticmethod
  def random_rgba(min_value=0, max_value=255, alpha=None):
    """Génère une couleur RGBA aléatoire en utilisant colorsys."""
    rgb = Colors.random_rgb(min_value, max_value)
    if alpha is None:
      alpha = random.randint(min_value, max_value)
    return (*rgb, alpha)

  @staticmethod
  def random_pastel():
    """Génère une couleur pastel aléatoire en utilisant colorsys."""
    h = random.random()
    s = random.uniform(0.2, 0.5)
    v = random.uniform(0.8, 1.0)
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    return (
      int(r * 255),
      int(g * 255),
      int(b * 255)
    )

  @staticmethod
  def random_dark():
    """Génère une couleur sombre aléatoire en utilisant colorsys."""
    h = random.random()
    s = random.uniform(0.5, 1.0)
    v = random.uniform(0.1, 0.3)
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    return (
      int(r * 255),
      int(g * 255),
      int(b * 255)
    )
  
  @staticmethod
  def random_saturated():
    """Génère une couleur très saturée aléatoire en utilisant colorsys."""
    h = random.random()
    s = 1.0
    v=1
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    return (
      int(r * 255),
      int(g * 255),
      int(b * 255)
    )
    
  @staticmethod
  def rainbow_color(n, nMax):
    """Renvoie une couleur arc-en-ciel pour n dans [0, nMax]."""
    n = (n + Colors.seed) % nMax
    if nMax == 0:
      h = 0
    else:
      h = float(n) / nMax
    r, g, b = colorsys.hsv_to_rgb(h, 1.0, 1.0)
    return (int(r * 255), int(g * 255), int(b * 255))
  
  @staticmethod
  def nuances_bleu(n, nMax):
    """Renvoie une nuance de bleu pour n dans [0, nMax], en parcourant les teintes bleues."""
    n = (n + Colors.seed) % nMax
    if nMax == 0:
      h = 0.6  # teinte bleue par défaut
    else:
      # h varie de ~0.55 (bleu turquoise) à ~0.75 (bleu-violet)
      h = 0.55 + 0.2 * (float(n) / nMax)
    r, g, b = colorsys.hsv_to_rgb(h, 1.0, 1.0)
    return (int(r * 255), int(g * 255), int(b * 255))
  
  @staticmethod
  def nuances_noir(n, nMax):
    """Renvoie une nuance de noir pour n dans [0, nMax]."""
    n = (n + Colors.seed) % nMax
    if nMax == 0:
      h = 0
    else:
      h = float(n) / nMax
    r, g, b = colorsys.hsv_to_rgb(h, 0.0, 1.0)
    return (int(r * 255), int(g * 255), int(b * 255))
  
  @staticmethod
  def nuances_rouge(n, nMax):
    """Renvoie une nuance de rouge pour n dans [0, nMax], en parcourant les teintes rouges."""
    n = (n + Colors.seed) % nMax
    if nMax == 0:
      h = 0.0  # teinte rouge par défaut
    else:
      # h varie de ~0.0 (rouge) à ~0.1 (rouge-orangé)
      h = 0.0 + 0.1 * (float(n) / nMax)
    r, g, b = colorsys.hsv_to_rgb(h, 1.0, 1.0)
    return (int(r * 255), int(g * 255), int(b * 255))

  @staticmethod
  def nuances_vert(n, nMax):
    """Renvoie une nuance de vert pour n dans [0, nMax], en parcourant les teintes vertes."""
    n = (n + Colors.seed) % nMax
    if nMax == 0:
      h = 0.33  # teinte verte par défaut
    else:
      # h varie de ~0.25 (vert-jaune) à ~0.45 (vert-bleu)
      h = 0.25 + 0.2 * (float(n) / nMax)
    r, g, b = colorsys.hsv_to_rgb(h, 1.0, 1.0)
    return (int(r * 255), int(g * 255), int(b * 255))

  @staticmethod
  def nuances_jaune(n, nMax):
    """Renvoie une nuance de jaune pour n dans [0, nMax], en parcourant les teintes jaunes."""
    n = (n + Colors.seed) % nMax
    if nMax == 0:
      h = 0.15  # teinte jaune par défaut
    else:
      # h varie de ~0.13 (jaune-orangé) à ~0.18 (jaune-vert)
      h = 0.13 + 0.05 * (float(n) / nMax)
    r, g, b = colorsys.hsv_to_rgb(h, 1.0, 1.0)
    return (int(r * 255), int(g * 255), int(b * 255))

  @staticmethod
  def nuances_violet(n, nMax):
    """Renvoie une nuance de violet pour n dans [0, nMax], en parcourant les teintes violettes."""
    n = (n + Colors.seed) % nMax
    if nMax == 0:
      h = 0.75  # teinte violette par défaut
    else:
      # h varie de ~0.7 (violet-bleu) à ~0.85 (violet-rose)
      h = 0.7 + 0.15 * (float(n) / nMax)
    r, g, b = colorsys.hsv_to_rgb(h, 1.0, 1.0)
    return (int(r * 255), int(g * 255), int(b * 255))

  @staticmethod
  def nuances_orange(n, nMax):
    """Renvoie une nuance d'orange pour n dans [0, nMax], en parcourant les teintes oranges."""
    n = (n + Colors.seed) % nMax
    if nMax == 0:
      h = 0.08  # teinte orange par défaut
    else:
      # h varie de ~0.05 (orange-rouge) à ~0.12 (orange-jaune)
      h = 0.05 + 0.07 * (float(n) / nMax)
    r, g, b = colorsys.hsv_to_rgb(h, 1.0, 1.0)
    return (int(r * 255), int(g * 255), int(b * 255))
  

  @staticmethod
  def random_nuance(n, nMax):
    """Choisit au hasard une des fonctions de nuance et l'applique à (n, nMax)."""
    if Colors.functionChosen is not None:
      return Colors.functionChosen(n, nMax)
    nuances = [
      Colors.nuances_bleu,
      Colors.nuances_noir,
      Colors.nuances_jaune,
      Colors.nuances_violet,
      Colors.nuances_orange,
      Colors.rainbow_color
    ]
    func = random.choice(nuances)
    Colors.functionChosen = func
    return func(n, nMax)