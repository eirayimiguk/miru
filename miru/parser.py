from typing import Tuple

class Parser:
    def novelai_diffusion(text: str, parsed_tag: dict) -> Tuple[str, list]:
        """
        Filename
            Pattern 1
                "tag, tag, tag, s-xxx.png" -> s-xxx, [tag, tag, tag]
            pattern 2
                "tag, tag, tag s-xxx.png" -> s-xxx, [tag, tag, tag]
            pattern 2
                "{tag}, {{tag}}, tag s-xxx.png" -> s-xxx, [tag, tag, tag]
        """
        filename, tags = text.rsplit(" ", 1)[1], text.rsplit(" ", 1)[0]
        tags = [x.strip().replace("{", "").replace("}", "").replace("(", "").replace(")", "") for x in tags.split(", ") if not x.strip() == '']
        tags = [{"name":tag} for tag in tags]
        tags.append(parsed_tag)

        return filename, tags
