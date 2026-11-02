# Chapter 2 parameter-space explanations and profile sequencing

Target: @HowToLens
Issue: https://github.com/PyAutoLabs/HowToLens/issues/123
Issued: 2026-11-02
Type: docs
Consequence: judge

## Original request (verbatim)
Lets continue working on chapter 2 of HowToLens using the same approach as before in the other chat, with these additional notes: 
- dont use or reference a linear light profile in tutorials 1, 2, 3, as theya re introduced and explained in4.
- I think chapter 2 has lot some of the descriptponof pa parameter space with the functions written out explciitly and 
- I think thats worth bringing back in, the detailed pheonmelogical descritpion is gone.
- as well as more live points modeling is hard should mention there are many different search methods and point to the optional
tutorial and that trying different ones also helps a lot.
- in why modelin gis hard be more explicit that the example we did above was a bit contributed by reducing n_live,
but the general truth is you will often encourage local maxima in lens model fits to real data, often it can be
difficult to work out for certain if your fit was a local or global maxima and therefore th3 approaches we outlines in this
tutorials ar techniques that allow us to overcome these issues through investigation as well as understand how modeling works
in more detial.

## Approved plan
Five full prose/code blocks approved in Codex chat 01a19c86-3bab-7183-a1e1-a04ff3e80c7f on 2026-11-02 ("yes this is good").
- Restore explicit one-, two- and N-dimensional likelihood functions and physical explanations in Tutorial 1.
- Use al.lp.ExponentialCoreSph with a searched intensity; remove linear-profile references throughout Tutorials 1–3.
- Explain the deliberately reduced live-point example, real-data local maxima and the limits of identifying a global maximum in Tutorial 3.
- Explain alternative search methods and link the optional searches tutorial.
- Regenerate notebooks/catalogue and validate syntax, math preservation, navigation and repository smoke.
Tier: judge — merge mode: human /prm. No merge authorized.

## Detailed scope
Edit scripts/chapter_2_lens_modeling/tutorial_1_non_linear_search.py, tutorial_2_practicalities.py and tutorial_3_why_modeling_is_hard.py only, plus generated counterparts/catalogue. Preserve the approved text from this chat, add More Dimensions to Contents, and remove inconsistent Analysis and wrap-up references. No changes to Tutorial 4 or later lessons. Existing chapter2_continuation.md still owns the later five-block reviews.
Branch: feature/howtolens-ch2-explanations
Worktree: /home/jammy/Code/PyAutoLabs/.worktrees/howtolens-ch2-explanations/HowToLens
