from fasttemplate.layouts._base import Asset, AssetDoesNotExistError, LayoutBase, Project


class LayoutManager:
    def __init__(self, project: Project, src: bool, asset: Asset, /) -> None:
        self.project: Project = project
        self.src: bool = src
        self.asset: Asset = asset

    def get_layout(self) -> LayoutBase:
        from fasttemplate.layouts.fastapi import Layout

        try:
            return Layout(self.project, self.asset, src=self.src)
        except AssetDoesNotExistError:
            raise
