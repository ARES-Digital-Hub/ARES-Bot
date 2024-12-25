import discord
import asyncio

class PaginationView(discord.ui.View):
    def __init__(self, pages):
        super().__init__(timeout=None)
        self.pages = pages
        self.current_page = 0
        self.update_footer()

    def update_footer(self):
        for i, page in enumerate(self.pages):
            page.set_footer(text=f"Page {i + 1} of {len(self.pages)}")

    @discord.ui.button(label="Previous", style=discord.ButtonStyle.primary)
    async def previous_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_page = (self.current_page - 1) % len(self.pages)
        await interaction.response.edit_message(embed=self.pages[self.current_page])

    @discord.ui.button(label="Next", style=discord.ButtonStyle.primary)
    async def next_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_page = (self.current_page + 1) % len(self.pages)
        await interaction.response.edit_message(embed=self.pages[self.current_page])


def create_multi_page_embed(title: str, description_list: list, color: discord.Color, items_per_page: int = 10):
    pages = []
    for i in range(0, len(description_list), items_per_page):
        embed = discord.Embed(
            title=title,
            description="\n".join(description_list[i:i+items_per_page]),
            color=color
        )
        pages.append(embed)
    return pages