class WebsitePaths:
    BaseWebsite = "https://yugipedia.com"
    CardData = "https://yugipedia.com/wiki/List_of_Yu-Gi-Oh!_Forbidden_Memories_cards"
    FusionData1 = "https://yugipedia.com/wiki/List_of_Yu-Gi-Oh!_Forbidden_Memories_Fusions_(001–200)"
    FusionData2 = "https://yugipedia.com/wiki/List_of_Yu-Gi-Oh!_Forbidden_Memories_Fusions_(201–400)"
    FusionData3 = "https://yugipedia.com/wiki/List_of_Yu-Gi-Oh!_Forbidden_Memories_Fusions_(401–600)"
    FusionData4 = "https://yugipedia.com/wiki/List_of_Yu-Gi-Oh!_Forbidden_Memories_Fusions_(601–722)"

    def return_all_fusion_websites(self):
        return [self.FusionData1, self.FusionData2, self.FusionData3, self.FusionData4]
