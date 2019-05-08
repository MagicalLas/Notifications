def test_create_group():
    sadistix_group = Group("Sadistix Coders", "Invite_key")
    assert isinstance(sadistix_group, Group)
    assert sadistix_group.name == "sadistix_coders"
    assert sadistix_group.invite_key == "invite_key"