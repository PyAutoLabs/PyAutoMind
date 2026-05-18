This is a conversation I had with Aris about implmeenting multipole light profiles, read it and then work it into
a plan. 

Note that I would be keen for us to make its API unified with ellipse multipole light profiles,w hich are now
fully support in JAX, so that light profiles multipole for galaxies can easily be extended to have
multiple multipoles without each individual light profile being defined as a specific combination.

Think hard, do deep research and come up with a plan for z_features:

Aris  [11:24 AM]
I have created a few new light profiles

Sersic + m3 + m4
Gaussian + m3 + m4

Should I open a autogalaxy issue and put them there so that if you want you can just paste them in?

I havent actually tried to implement it but I am assuming it is straightforward to make a (Gaussian + m=3,4) MGE model?
Jam  [11:27 AM]
Yeah if you put an issue up I'll get Claude to do it.
[11:28 AM]Do they mirror mass profile multiples in so far that they are just the image of the mulitpole (e.g. mass is just deflections) or are they the whole image kf the swrsic and gaussian?
Aris  [11:32 AM]
The amplitudes should mirror what we get from multipole mass models but the implementation logic is different.

For light profiles you perturb the grid_radii (the logic is similar to the perturbed ellipses from ellipse fitting) so the profile is evaluated at different positions.
Jam  [11:34 AM]
Ah right let's just implement them as standalone light profiles for now then, and future work can generalise multiples to be an extension of light profiles so we avoid Gaussian + m1 + m3 + m4 and the like
[11:35 AM]Albeit that'll br a brief follow up claude issue provided we have a few good test cases in place
[11:36 AM]Maybe I can unify the API with ellipse fitting
Aris  [11:36 AM]
class SersicPert(AbstractSersic, LightProfile):
    """
    A Sersic light profile with m=3 and m=4 Fourier perturbations.

    The eccentric radius is perturbed as:

        r_perturbed = r * (
            1
            + m3_0 * cos(3θ)
            + m3_1 * sin(3θ)
            + m4_0 * cos(4θ)
            + m4_1 * sin(4θ)
        )

    where:
        - r is the eccentric radius
        - θ is the polar angle in the profile frame
    """

    def __init__(
        self,
        centre: Tuple[float, float] = (0.0, 0.0),
        ell_comps: Tuple[float, float] = (0.0, 0.0),
        intensity: float = 0.1,
        effective_radius: float = 0.6,
        sersic_index: float = 4.0,
        m3_0: float = 0.0,
        m3_1: float = 0.0,
        m4_0: float = 0.0,
        m4_1: float = 0.0,
    ):
        super().__init__(
            centre=centre,
            ell_comps=ell_comps,
            intensity=intensity,
            effective_radius=effective_radius,
            sersic_index=sersic_index,
        )

        self.m3_0 = m3_0
        self.m3_1 = m3_1

        self.m4_0 = m4_0
        self.m4_1 = m4_1

    @property
    def m3_amplitude(self):
        return (self.m3_0**2 + self.m3_1**2) ** 0.5

    @property
    def m3_phi(self):
        return np.arctan2(
            self.m3_1,
            self.m3_0,
        ) / 3.0

    @property
    def m4_amplitude(self):
        return (self.m4_0**2 + self.m4_1**2) ** 0.5

    @property
    def m4_phi(self):
        return np.arctan2(
            self.m4_1,
            self.m4_0,
        ) / 4.0

    def perturbed_radii_from(
        self,
        grid,
        xp=np,
        **kwargs,
    ):
        """
        Returns Fourier-perturbed eccentric radii.
        """

        # IMPORTANT:
        # Extract raw backend array for JAX compatibility

        grid_array = grid.array

        y = grid_array[:, 0]
        x = grid_array[:, 1]

        grid_radii = self.eccentric_radii_grid_from(
            grid=grid,
            xp=xp,
            **kwargs,
        )

        # grid_radii may also be an AA wrapper
        if hasattr(grid_radii, "array"):
            grid_radii = grid_radii.array

        theta = xp.arctan2(y, x)

        perturbation = (
            1.0
            + self.m3_0 * xp.cos(3.0 * theta)
            + self.m3_1 * xp.sin(3.0 * theta)
            + self.m4_0 * xp.cos(4.0 * theta)
            + self.m4_1 * xp.sin(4.0 * theta)
        )

        perturbed_radii = grid_radii * perturbation

        perturbed_radii = xp.maximum(
            perturbed_radii,
            1e-8,
        )

        return perturbed_radii

    def image_2d_via_radii_from(
        self,
        grid_radii,
        xp=np,
        **kwargs,
    ):
        """
        Returns the Sersic image evaluated at input radii.
        """

        return self._intensity * xp.exp(
            -self.sersic_constant
            * (
                (grid_radii / self.effective_radius)
                ** (1.0 / self.sersic_index)
                - 1.0
            )
        )

    @aa.over_sample
    @aa.grid_dec.to_array
    @check_operated_only
    @aa.grid_dec.transform
    def image_2d_from(
        self,
        grid: aa.type.Grid2DLike,
        xp=np,
        operated_only: Optional[bool] = None,
        **kwargs,
    ) -> aa.Array2D:
        """
        Returns the 2D image of the perturbed Sersic profile.
        """

        perturbed_radii = self.perturbed_radii_from(
            grid=grid,
            xp=xp,
            **kwargs,
        )

        return self.image_2d_via_radii_from(
            grid_radii=perturbed_radii,
            xp=xp,
            **kwargs,
        )chatgpt didnt use ell_comps for the parameters but this is a super easy fix, should I just put it like that
Jam  [11:37 AM]
Does this work for elliptical multiples then?
[11:37 AM]And do we have code for elliptical multiples of ellipse fitting?
Aris  [11:37 AM]
so for the light profiles, because you are perturbing the grid_radii, the perturbation follows the ellipticity of the grid (edited) 
Jam  [11:37 AM]
Put it up like that but leave a note on ell comps
Aris  [11:37 AM]
so this is more like a elliptical multipole
[11:38 AM]so the ellipse fitting as well is more like "elliptical multipoles" (edited) 
Jam  [11:39 AM]
Isn't our ellipse fitting multiples code still spherical like? Anyway there is a logical way to unify these image light profiles with ellipse fitting include that.
[11:39 AM]I am JAX ING ellipse fitting this week for Sam so it's good timing all round haha
Aris  [11:42 AM]
If I understand this correctly the ellipse fitting is more like elliptical mass model multipoles because the perturbation we are adding is applied directly to an already ellptical path. The Paugnet paper actually discussed this specifically referencing out m1 paper