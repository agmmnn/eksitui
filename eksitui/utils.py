def smalltext(txt: str, type: int = 1) -> str:
    inp = "qwertyuiopasdfghjklzxcvbnmğüşıöç1234567890()-'+=?!$"
    super_chars = "ᑫʷᵉʳᵗʸᵘⁱᵒᵖᵃˢᵈᶠᵍʰʲᵏˡᶻˣᶜᵛᵇⁿᵐᵍᵘᶳᶥᵒᶜ¹²³⁴⁵⁶⁷⁸⁹⁰⁽⁾⁻'⁺⁼ˀꜝᙚ"
    sub_chars = "ₐₑₕᵢₖₗₘₙₒₚᵣₛₜᵤᵥₓ₁₂₃₄₅₆₇₈₉₀₊₌₍₎₋₋₋₋₋₋₋₋₋₋₋₋₋₋₋₋₋₋₋₋₋"
    return txt.translate(str.maketrans(inp, super_chars if type else sub_chars))
