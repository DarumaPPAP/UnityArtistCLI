# ArtistSubAgent Backend Package ID migration

Current canonical Unity Package ID:

```text
com.darumappap.artist-subagent
```

Legacy beta Package ID:

```text
com.darumappap.unity-artist
```

The rename is intentional. `com.darumappap.unity-artist` was named after the old UnityArtistCLI product surface, while the current package is the Unity Editor backend package required by `artist_subagent`.

For new installations, use only `com.darumappap.artist-subagent`. Existing projects pinned to the old beta package must replace the dependency key and Git/local package path explicitly; Unity Package Manager does not treat a package-ID rename as an in-place upgrade.

The identities remain separate:

- Specialist: `artist_subagent`
- Backend/provider: `unity_artist_cli`
- Host executable: `unity-artist`
- Unity package: `com.darumappap.artist-subagent`
