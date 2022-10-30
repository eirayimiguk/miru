from typing import Tuple

class Parser:
    def novelai_diffusion(text: str) -> Tuple[str, list]:
        """
        Filename
            Pattern 1
                "tag, tag, tag, filename.png"
            Pattern 2
                "tag, tag, tag filename.png"
        """
        filename, tags = text.rsplit(" ", 1)[1], text.rsplit(" ", 1)[0]
        tags = [x.strip() for x in tags.split(", ") if not x.strip() == '']
        tags = [{"name":tag} for tag in tags]
        tags.append({"name": "miru-parsed"})

        return filename, tags
