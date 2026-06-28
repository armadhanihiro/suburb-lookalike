from dataclasses import dataclass


@dataclass
class GoldenReference:
    reference: str
    expected: list[str]
    rationale: str


GOLDEN_SET: list[GoldenReference] = [
    # Cluster 0
    GoldenReference(
        reference="Birkdale - Queensland",
        expected=[
            "Wellington Point - Queensland",
            "Elanora - Queensland",
            "Box Head - MacMasters Beach - New South Wales",
            "Springwood - Winmalee - New South Wales",
            "Mount Martha - Victoria",
        ],
        rationale=(
            "Selected using combined hybrid similarity and KPI similarity. "
            "These neighbours were chosen because they ranked highly under the "
            "hybrid model while also maintaining close demographic KPI patterns."
        ),
    ),

    # Cluster 1
    GoldenReference(
        reference="Ingleburn - New South Wales",
        expected=[
            "Blacktown - South - New South Wales",
            "Minto - St Andrews - New South Wales",
            "Hadfield - Victoria",
            "Altona North - Victoria",
            "Glendenning - Dean Park - New South Wales",
        ],
        rationale=(
            "Selected using combined hybrid similarity and KPI similarity. "
            "These neighbours were chosen because they ranked highly under the "
            "hybrid model while also maintaining close demographic KPI patterns."
        ),
    ),

    # Cluster 2
    GoldenReference(
        reference="Bega - Tathra - New South Wales",
        expected=[
            "Gympie - South - Queensland",
            "Tatiara - South Australia",
            "King Island - Tasmania",
            "Summerhill - Prospect - Tasmania",
            "Kangaroo Island - South Australia",
        ],
        rationale=(
            "Selected using combined hybrid similarity and KPI similarity. "
            "These neighbours were chosen because they ranked highly under the "
            "hybrid model while also maintaining close demographic KPI patterns."
        ),
    ),

    # Cluster 3
    GoldenReference(
        reference="Halls Creek - Western Australia",
        expected=[
            "Victoria River - Northern Territory",
            "Gulf - Northern Territory",
            "Tanami - Northern Territory",
            "Elsey - Northern Territory",
            "Barkly - Northern Territory",
        ],
        rationale=(
            "Selected using combined hybrid similarity and KPI similarity. "
            "These neighbours were chosen because they ranked highly under the "
            "hybrid model while also maintaining close demographic KPI patterns."
        ),
    ),

    # Cluster 4
    GoldenReference(
        reference="Bibra Industrial - Western Australia",
        expected=[
            "Welshpool - Western Australia",
            "Koolpinyah - Northern Territory",
            "Migratory - Offshore - Shipping (NT) - Northern Territory",
            "Migratory - Offshore - Shipping (WA) - Western Australia",
            "Prospect Reservoir - New South Wales",
        ],
        rationale=(
            "Selected using combined hybrid similarity and KPI similarity. "
            "These neighbours were chosen because they ranked highly under the "
            "hybrid model while also maintaining close demographic KPI patterns."
        ),
    ),

    # Cluster 5
    GoldenReference(
        reference="Aitkenvale - Queensland",
        expected=[
            "Innisfail - Queensland",
            "Mildura - North - Victoria",
            "Newnham - Mayfield - Tasmania",
            "Kirwan - East - Queensland",
            "Newtown (Qld) - Queensland",
        ],
        rationale=(
            "Selected using combined hybrid similarity and KPI similarity. "
            "These neighbours were chosen because they ranked highly under the "
            "hybrid model while also maintaining close demographic KPI patterns."
        ),
    ),

    # Cluster 6
    GoldenReference(
        reference="Jindalee - Mount Ommaney - Queensland",
        expected=[
            "Seventeen Mile Rocks - Sinnamon Park - Queensland",
            "McDowall - Queensland",
            "Carindale - Queensland",
            "Belmont - Gumdale - Queensland",
            "Asquith - Mount Colah - New South Wales",
        ],
        rationale=(
            "Selected using combined hybrid similarity and KPI similarity. "
            "These neighbours were chosen because they ranked highly under the "
            "hybrid model while also maintaining close demographic KPI patterns."
        ),
    ),

    # Cluster 7
    GoldenReference(
        reference="Abbotsford - Victoria",
        expected=[
            "Prahran - Windsor - Victoria",
            "Brunswick East - Victoria",
            "Brunswick - South - Victoria",
            "South Yarra - West - Victoria",
            "Hobart - Tasmania",
        ],
        rationale=(
            "Selected using combined hybrid similarity and KPI similarity. "
            "These neighbours were chosen because they ranked highly under the "
            "hybrid model while also maintaining close demographic KPI patterns."
        ),
    ),

    # Cluster 8
    GoldenReference(
        reference="Subiaco - Shenton Park - Western Australia",
        expected=[
            "Elsternwick - Victoria",
            "Hawthorn East - Victoria",
            "Kensington (Vic.) - Victoria",
            "South Perth - Kensington - Western Australia",
            "Lyons (ACT) - Australian Capital Territory",
        ],
        rationale=(
            "Selected using combined hybrid similarity and KPI similarity. "
            "These neighbours were chosen because they ranked highly under the "
            "hybrid model while also maintaining close demographic KPI patterns."
        ),
    ),

    # Cluster 9
    GoldenReference(
        reference="Pallara - Willawong - Queensland",
        expected=[
            "Edmondson Park - New South Wales",
            "Coombs - Australian Capital Territory",
            "Denham Court - Bardia - New South Wales",
            "Schofields - East - New South Wales",
            "Leppington - Catherine Field - New South Wales",
        ],
        rationale=(
            "Selected using combined hybrid similarity and KPI similarity. "
            "These neighbours were chosen because they ranked highly under the "
            "hybrid model while also maintaining close demographic KPI patterns."
        ),
    ),

]