from pydantic import BaseModel, ConfigDict, Field, RootModel


class Post(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    user_id: int = Field(alias="userId")
    id: int
    title: str
    body: str


class PostList(RootModel):
    root: list[Post]

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]
