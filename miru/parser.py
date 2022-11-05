class NAIDiffusion:
    def __init__(self):
        self.parsed_tag = "NovelAI"

    def parse(self, text: str) -> list:
        """
        parsed_tag
            {"name": "tag"}

        Filename
            Pattern 1
                "tag, tag, tag, s-xxx.png" -> s-xxx, [tag, tag, tag]
            pattern 2
                "tag, tag, tag s-xxx.png" -> s-xxx, [tag, tag, tag]
            pattern 2
                "{tag}, {{tag}}, tag s-xxx.png" -> s-xxx, [tag, tag, tag]
        """
        tags = [x.replace("_", " ").replace("{", "").replace("}", "").replace("(", "").replace(")", "").strip() for x in text.split(",") if not x.strip() == '']
        tags = [{"name":tag} for tag in tags]
        tags.append({"name": self.parsed_tag})

        return tags
