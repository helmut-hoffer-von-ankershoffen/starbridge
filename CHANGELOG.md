[![starbridge](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/blob/main/tests/fixtures/starbridge.png?raw=true)](https://helmuthva.gitbook.io/starbridge) Starbridge

## [unreleased]

### ⛰️  Features

- *(web)* Provide tool to fetch from the web, respecting robots.txt and getting additional context from llms.txt - ([fc3ffeb](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/fc3ffeb88ceb7be3bc6d212df35b867f48550606))

### 🚜 Refactor

- *(init)* Simplify - ([703c278](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/703c2781a8967203c0ae0e49b0a11b3b31de1577))

### 🧪 Testing

- *(env)* Use subprocess in test_env_args_fail as --env is parsed on boot - ([de0a1d9](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/de0a1d9d699ed1bfb4a665856da10a8633da2b78))
- *(web)* More tests - ([91ab1d3](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/91ab1d33917fe3a5ad1e9740aba9ea59d8c2397f))

### ⚙️ Miscellaneous Tasks

- *(ruff)* Auto-fix and use preview checks - ([5f360bc](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/5f360bc54cc16ed178d2ef3ec618a9116fbf4650))
- *(style)* Formatting - ([bcc84ed](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/bcc84ed06e5033fa57b378d4fd65f8f630aede0f))


## [0.0.51](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/compare/v0.0.50..v0.0.51) - 2024-12-27

### 🚜 Refactor

- *(MCPBaseService)* Annotate abstract methods - ([9192372](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/91923723ba803394228ee23a505aedf688bb3b77))
- *(cli)* Dynamically discover settings to prompt for - ([7594f87](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/7594f87b34f57d69446015b6127fbcf1361892d9))
- *(cli)* Simplify - ([446145f](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/446145f6b1349661d3575dbb23657671b6aaff6c))
- *(di)* Introduce dependency injection (di) util, untie service->cli dependency - ([2b92828](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/2b92828fafd565fed43f034836919b83f43326db))

### 🎨 Styling

- *(ruff)* Pivot to defaults - ([ac35236](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/ac35236f8443ee1fa2f9fcd53d9e23b8a152e02e))


## [0.0.50](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/compare/v0.0.49..v0.0.50) - 2024-12-26

### 🧪 Testing

- *(extras)* Test for imaging extra not activated - ([dd5b4bb](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/dd5b4bbd8fa9510a04bb7aba840fb39d9e7c482c))

### ⚙️ Miscellaneous Tasks

- *(imaging)* Make imaging an extra - ([ffac1da](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/ffac1dae615724a10aa48522ab653168d434209a))


## [0.0.49](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/compare/v0.0.48..v0.0.49) - 2024-12-26

### 🧪 Testing

- *(confluence)* More cli commands - ([758f980](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/758f980bf9caf9881170df7b0164e7cf98408af1))

### ⚙️ Miscellaneous Tasks

- *(devcontainer)* Polish - ([cda9326](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/cda932604f2871fdbb84fb9b73f324ee02376a2e))
- *(devcontainer)* Enable docker in docker for docker tests in devcontainer - ([6f5554e](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/6f5554e1ac8d3b2a8b8e76de4b2671f12d3f3a06))


## [0.0.48](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/compare/v0.0.47..v0.0.48) - 2024-12-25

### 📚 Documentation

- *(badges)* Adapt to change of workflow name - ([92be681](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/92be681aa2e81300b0d17ddf9a473eda7b9063a7))
- *(badges)* Style Ruff - ([60178b7](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/60178b759b1f7c041c6bffb301c96e0fd2e83348))
- *(readme)* Intro - ([c1966fb](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/c1966fbe4ae3d2d3c141ca75e61aed7680f61816))

### ⚙️ Miscellaneous Tasks

- *(pre-commit)* Additional hooks - ([dea9820](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/dea9820bf47ea93ad5d73b35c156a9be5dc7b769))
- *(sonarqube)* Metas - ([26b6e8a](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/26b6e8af3677c15cbc223ac75d7b8f303660049d))
- *(sonarqube)* Tags - ([b08d11b](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/b08d11b593acf295b0a0fd004f130a63d32a331a))


## [0.0.46](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/compare/v0.0.45..v0.0.46) - 2024-12-24

### 🚜 Refactor

- *(mcp)* Auto-discover services, instead of having to enumerate them in pyproject.toml - ([fcd09a8](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/fcd09a860c7a73e18846bec0d88af7b05b11f745))

### 🧪 Testing

- *(Claude)* Health - ([799b818](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/799b8183de6e0c89fccd8a0c400f580dba7dbc44))
- *(confluence)* Cli commands - ([b2f086e](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/b2f086eb29b04660cbaef4886c2dd4a131aa2935))

### ⚙️ Miscellaneous Tasks

- *(bump)* Enable to specify version part to bump, default being patch - ([56709d7](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/56709d75ce6176cb5fc1fe2c52df6183153ac0ac))
- *(codecov)* Coverage > 80% now required - ([2b4d18c](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/2b4d18c1d23192171a39c58a83ba464dda1f3c7e))
- *(codecov)* Sensible green range - ([a754964](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/a754964ca7f95245974287c013e95b2dccdae8bf))


## [0.0.45](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/compare/v0.0.44..v0.0.45) - 2024-12-24

### 🧪 Testing

- *(docker)* Use docker-compose and pytest-docker plugin to test e2e from docker buildx to inspector started by starbridge controller - ([0fe9c49](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/0fe9c49f4b3a39312d1a83e20b2775e515d3b8d8))
- *(env)* Test --env not supported by all commands - ([9d30e64](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/9d30e64aaa0782f90d83c2b503262f584e6d667c))
- *(env)* Setting env via args - ([6b4f75f](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/6b4f75fbfd60bd7a27b0cba54f86d5362137eb3d))
- *(mcp)* Inspector reactivated - ([753ced8](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/753ced80587b5786cb42ca4f98479493e7b1c0ad))
- *(parallel)* Enable that tests marked as sequential can run as such, use for one that changes the environment on disk - ([22c1b53](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/22c1b531b5df94f9612f72481c303bc62e101115))

### ⚙️ Miscellaneous Tasks

- *(test)* Superfluous checkout - ([88534f3](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/88534f3b86c507eb61a4c92315add12c2c1d148c))


## [0.0.44](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/compare/v0.0.43..v0.0.44) - 2024-12-24

### 📚 Documentation

- *(badges)* Consolidate to shields.io - ([a237a46](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/a237a46f476e378ec5d0dadfded69f20ad8646a0))
- *(pypi)* Define supported python versions - ([bea82aa](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/bea82aa8ec04db7622f886835fed8c643cf73c9d))

### 🎨 Styling

- *(badges)* Consolidate labels - ([2630832](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/263083262830b4c1ceaebbbb3d2bfd75ef05a122))
- *(badges)* Use CD for github, pypi and docker - ([a300b36](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/a300b36867da42b1eb2b5af59635c5ff849b692f))


## [0.0.43](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/compare/v0.0.42..v0.0.43) - 2024-12-24

### ⚙️ Miscellaneous Tasks

- *(docker)* Set docker tags from semver tags - ([7d236c2](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/7d236c24fff1d52c5bc7a8804e1245608ce00eab))


## [0.0.42](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/compare/v0.0.41..v0.0.42) - 2024-12-24

### 📚 Documentation

- *(CHANGELOG.md)* Introduce in repo - ([78e11aa](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/78e11aa5400fba9803dbbc1793b4eadba6271976))


## [0.0.41](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/compare/v0.0.40..v0.0.41) - 2024-12-24

### ⚙️ Miscellaneous Tasks

- *(bump-my-version)* Update uv.lock on bumping - ([fa60f12](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/fa60f12ba5d6718d1b52ddd0852fcad0b1b2efed))


## [0.0.40](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/compare/v0.0.39..v0.0.40) - 2024-12-24

### ⚙️ Miscellaneous Tasks

- *(bump-my-version)* Update uv.lock on bumping - ([f1e2b52](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/f1e2b52ddf61d11ec3d7449fd42497e873891728))


## [0.0.39](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/compare/v0.0.38..v0.0.39) - 2024-12-24

### ⚙️ Miscellaneous Tasks

- *(docker)* Set docker tags from semver tags - ([1d1ae38](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/1d1ae38ef368edf177843b6e6a1d4ee9527818a9))


## [0.0.38](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/compare/v0.0.37..v0.0.38) - 2024-12-23

### ⚙️ Miscellaneous Tasks

- *(git-cliff)* Fix - ([7ab4ff7](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/7ab4ff7485ffe09bc9f089520b089115ae0167e1))


## [0.0.37](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/compare/v0.0.36..v0.0.37) - 2024-12-23

### ⚙️ Miscellaneous Tasks

- *(pytest)* Run tests in parallel - ([103b73e](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/103b73e609b2254f1cd1f7713ce70cee6c57c7e7))


## [0.0.36](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/compare/v0.0.35..v0.0.36) - 2024-12-23

### ⚙️ Miscellaneous Tasks

- *(git-cliff)* Unique - ([5badb97](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/5badb97d3452ec09fc6aae137cf0c3860f5da9e6))


## [0.0.35](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/compare/v0.0.34..v0.0.35) - 2024-12-23

### ⚙️ Miscellaneous Tasks

- *(bump)* Utility - ([4e9cb39](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/4e9cb3990fedd83b047636bc322736fa66539a64))


## [0.0.34](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/compare/v0.0.33..v0.0.34) - 2024-12-23

### ⚙️ Miscellaneous Tasks

- *(bump)* Utility - ([c931fe6](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/c931fe6aa6c326fcecbbda86824b5f0ca91b135b))


## [0.0.33](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/compare/v0.0.32..v0.0.33) - 2024-12-23

### ⚙️ Miscellaneous Tasks

- *(git-cliff)* Don't use typos - ([9fd5184](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/9fd5184609975633e884fb217f7ddaa2f89b5509))


## [0.0.32](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/compare/v0.0.31..v0.0.32) - 2024-12-23

### ⚙️ Miscellaneous Tasks

- *(git-cliff)* Test - ([737a9a3](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/737a9a32d68222b9070cd9090970f6ad42a9beff))


## [0.0.31](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/compare/v0.0.30..v0.0.31) - 2024-12-23

### ⚙️ Miscellaneous Tasks

- *(pre-commit)* Improve handling - ([9615aeb](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/9615aebdd7e062d2de054cd08b16e38969576651))


## [0.0.30](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/compare/v0.0.29..v0.0.30) - 2024-12-23

### ⚙️ Miscellaneous Tasks

- *(detect-secrets)* Introduce - ([b16bc64](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/b16bc647b95fa70a9066f66c0d31fa4a9bdaa654))


## [0.0.29](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/compare/v0.0.28..v0.0.29) - 2024-12-23

### 📚 Documentation

- Mention renovate - ([0bbebb0](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/0bbebb09a2a6d2934b628bd67bf1c50cdbe434b0))
- Update keywords to match tooling - ([5408c26](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/5408c262000ac25400d87c8b1015ccbff37e69d4))

### 🧪 Testing

- *(coverage)* Omit instrumentation - ([813a576](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/813a576d10fb5e59d053b3e5579423c9e8cbf010))
- *(mcp)* Sse basics - ([faa0e78](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/faa0e788ccb44f87cef02f7c39667a7c0b3bc9f4))
- *(mcp)* Binary resource - ([956bbc0](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/956bbc096e005bab1e7bf5d512a4331397052019))
- *(mcp)* Inspector - ([d1704b2](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/d1704b2b6ca8a3bbabeb95f30df2dbf199f0030f))
- Relative? - ([27ffab3](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/27ffab3377665d19834f6c84236c04bb81ade319))
- More - ([ef3b4fe](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/ef3b4fed8b2397ea87821207ab84f97b6dbb4362))
- ... - ([acf7e13](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/acf7e139ac572b4f18e5fce56aae2aaea4b0ed49))
- Trial - ([b516a0c](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/b516a0c6d06bcc74d11718394afb59c7011f5bc2))

### ⚙️ Miscellaneous Tasks

- *(bump-my-version)* Config - ([3e8495f](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/3e8495f114cda6811bc938c08f1ce7a3b78608c5))
- *(sonarqube)* Signal we have to be compatible with 3.11 so we cannot use the new type parameter syntax of Python 3.12 - ([4146430](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/41464302f77c083c80458a074f4897e33bfe2f9a))
- *(sonarqube)* No shallow clone - ([34c1473](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/34c1473483385425f3c8b519f95a5d9ca01da094))
- *(sonarqube)* Exclude node_modules - ([77d164d](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/77d164d5a0735a5bd6acf6f748b3b0f3acdaf1d4))
- *(sonarqube)* Exclusions - ([69f6913](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/69f69131927a3e087a3df6e20864b16a0c74935f))
- *(sonarqube)* Issue - ([787dceb](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/787dceb5c93dc4c806eebf7ef8660e496a692d00))
- Introduce bump-my-version - ([e5882d4](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/e5882d431f9378aff9ea5496cba19f1437e1b5ea))
- Reenable pre-commit hook - ([a7f1117](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/a7f1117ba95fe0a60e4cc68975f3d35663f6e8d3))

### ◀️ Revert

- Test all versions in pre-commit - ([072e711](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/072e711d528971b234dc9aaadd1bcbfeb2068abf))

### Change

- VERSION - ([a022593](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/a02259381135236a5cb4e9e1955d658bb957502a))
- File placement - ([ad2451f](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/ad2451f78fa0cd2413e1532a41adaa54ea80350f))

### Enh

- *(cairo)* User friendly error display if not installed - ([6cb8aac](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/6cb8aacdc3080a36d63ec79f8638cf44ccbdf691))

### Enh/doc

- *(Docker)* Polish a bit - ([17551f5](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/17551f5bf564ecb0cba3b79f647f475da08b0720))


## [0.0.28](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/compare/v0.0.27..v0.0.28) - 2024-12-22

### 🐛 Bug Fixes

- *(docker)* Typo - ([dda0c91](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/dda0c919957fd5800b43f7e827e582a0c5091750))

### 🚜 Refactor

- *(mcp)* Reduce complexity - ([8bc1b6f](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/8bc1b6f87115ae4682b07a20fb75689365ba1773))
- *(sonarqube)* A few issues identified - ([e092e58](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/e092e58470c0bf8f7424848bc93a3209b0105af1))

### 📚 Documentation

- *(gitbook)* Link - ([4a08b83](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/4a08b83ed770c7e7a9a8a57151ceab993b29e86f))
- Github activity badge - ([420e052](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/420e0522e5d9d2a29d2db49a2de19b5877596137))
- Sonarqube badges - ([38aa531](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/38aa53144e2cbfd09a8faab73ce5194f9195ba37))

### 🧪 Testing

- *(claude)* Log - ([7c51114](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/7c51114b454f2f2ade2893223d132294777c69f7))
- *(confluence)* Fix missing mock - ([2c9abbf](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/2c9abbfdcc0d740c0d236eae0cc503bd946a5e80))
- *(inspector)* Enough for today - ([08cccfa](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/08cccfadc97247014a93e3a87fb383057472c015))
- *(sonarqube)* More - ([8156649](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/8156649c06711a148972bbfc441c123ed015df10))
- *(sonarqube)* To reach quality gate - ([46600f3](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/46600f3d06b9d9da244bfd0d89580311eca3dba5))
- > 80% - ([6b75807](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/6b75807841e1ff2e4e975bfce10357ebf5024a0a))

### ⚙️ Miscellaneous Tasks

- *(sonarqube)* Switch to CI mode - ([df26e87](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/df26e879301cf8c05ce4de315f4318419ecd2c64))
- *(sonqarqube)* Coverage to not include build tools - ([f320564](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/f3205648ecbf3478f99880f39b21fa42e92a8836))

### Security

- *(sonarqube)* Enforce SSL on nodejs setup - ([01b811d](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/01b811d607746eae6a927ed9fa324ccb894081df))
- Do not silently install recommended packages - ([02e7ef1](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/02e7ef1c7fc1bd2f56eb2e690262fb4ea7b7b464))


## [0.0.27](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/compare/v0.0.26..v0.0.27) - 2024-12-21

### 🐛 Bug Fixes

- *(test)* Claude restart not supported on linux - ([26e0e36](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/26e0e360e2b9e4c3b4978ea0d3a3d150a274f6c5))
- *(test)* Starbridge.png - ([a10d2d3](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/a10d2d360f554fa616d536dab65080f21f152223))

### 📚 Documentation

- *(badge)* Docker - ([2643ddb](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/2643ddbb871cbc048309cc440fbbcaddf8f71a61))
- Badge name - ([5e29216](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/5e292164e2bc3c95abeb23d2f5fe69e3ef60164d))

### 🧪 Testing

- *(fix)* No restart on test for uninstall - ([9632421](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/96324212420cfe7c7e60aa8d238508378e7599c8))

### ⚙️ Miscellaneous Tasks

- *(release)* V0.0.27 - ([5066b2b](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/5066b2bd99a9f700e70efca958ab51b5f3727077))


## [0.0.26](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/compare/v0.0.25..v0.0.26) - 2024-12-21

### 🧪 Testing

- *(cli,mcp,env)* More - ([89eb328](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/89eb328bb5eb396b676f763ad53fbae72f1cb5e2))


## [0.0.25](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/compare/v0.0.24..v0.0.25) - 2024-12-21

### 🐛 Bug Fixes

- Indicate exit on fail - ([8b3e4e0](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/8b3e4e0ee5f592e92ba95808ed424d69afc4af47))
- Epilog - ([753bb92](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/753bb9243284179f16a3a8f0f35c000fa698ad45))
- Missing dependency in github action - ([1a723d1](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/1a723d17692baeee74209cd93d1c3a3e874175ca))

### 🚜 Refactor

- *(cli)* No args is help auto-set for groups - ([cd9ff88](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/cd9ff88871eb57240e5603155f2b453150ce6a08))

### 📚 Documentation

- Fix - ([790ddcd](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/790ddcd1ba52fbc022fbf9372ca4af3c27fae034))

### 🧪 Testing

- *(claude,hello)* A bit - ([8f5593f](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/8f5593f67700ab500415cd65789c4a5586da1a84))
- *(mcp)* Enable cross-process mocks with fixture - ([6713c83](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/6713c832910004f755ad42660f8759ed0343f2a3))
- *(mcp)* More tests, and test-coverage across processes - ([e47cc49](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/e47cc498427b64ac765f28f4423c5a1d5c93757b))
- *(mcp)* Start - ([3f3c282](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/3f3c2825e314abfb00243615aea7c75cf12c580d))
- Fix - ([bf48cc8](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/bf48cc8c0a896fa2e57e51b8b0353bd6a3d219a4))

### ⚙️ Miscellaneous Tasks

- *(test)* Upload test executions to codecov - ([873ddb7](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/873ddb7a59cb34b0b36cfc57e889bc6bd582a440))

### Change

- Epilog - ([d6d52d1](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/d6d52d1dcd4c59d8c8fddb033f0c311984511096))

### Enh

- *(logging)* Fatal is an alias of critical - ([8105621](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/81056216958cc02ac4bc1554cd5cc446c11bd541))


## [0.0.24](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/compare/v0.0.23..v0.0.24) - 2024-12-21

### 🚜 Refactor

- Health, enh: logging - ([cee8c75](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/cee8c7518a4e42f6458aecab70433a0ad3d43074))

### GITBOOK-2

- No subject - ([844301c](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/844301cf994b4e46be4bd4f82cfe6b62372dccea))


## [0.0.23](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/compare/v0.0.22..v0.0.23) - 2024-12-20

### ⚙️ Miscellaneous Tasks

- Polish for otel instrumentation - ([05bcc12](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/05bcc12d1c727ca9b2f909e0eb150ceeff0735f9))


## [0.0.22](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/compare/v0.0.21..v0.0.22) - 2024-12-20

### 🐛 Bug Fixes

- .env.example for Docker - ([059e16e](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/059e16ee3c8525c52336b7440e905ea3dbbc2b57))


## [0.0.21](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/compare/v0.0.20..v0.0.21) - 2024-12-20

### ⚙️ Miscellaneous Tasks

- Release 0.0.21 - ([1155f73](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/1155f73e2cadcd34adeab966a5bb2c5a6ad6f877))


## [0.0.20](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/compare/v0.0.19..v0.0.20) - 2024-12-20

### 📚 Documentation

- Keywords - ([b0668ef](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/b0668ef4807d18fc921b70c1d73b3ce7cedbf1f9))
- Some - ([ced4f86](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/ced4f865f78df9499dc43463bce7c69154d7f2a1))


## [0.0.19](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/compare/v0.0.18..v0.0.19) - 2024-12-20

### 🐛 Bug Fixes

- *(test)* Env.example - ([39fcd4a](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/39fcd4a4b8c98272dc363d6c911873077f35dc2d))
- Various - ([2fd7c4f](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/2fd7c4f60dafea6921303b96c034becebf678a29))

### 🧪 Testing

- Enable matrix-testing - ([7da1576](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/7da15766393b5e49774d7e7541183773d5b13601))

### ⚙️ Miscellaneous Tasks

- Release 0.0.19 - ([fa8294f](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/fa8294fb832e9e02bda89aaeb0bb37facfdf65ba))
- Focus on own code in pylance - ([d2c50a1](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/d2c50a19468dbeab53ee804e456822fa547ae078))

### Cont

- *(instrumentation)* Some - ([89cb601](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/89cb6010c02231fbea8370b43ef1087226c4989c))


## [0.0.18](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/compare/v0.0.17..v0.0.18) - 2024-12-19

### 📚 Documentation

- *(Docker)* Polish - ([5746e83](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/5746e8308f92db5cb3597e0d0ad07539378e0b15))

### V0.0.18

- Docker polish - ([46e05ec](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/46e05ec2a7b310d380da9824a9f1ecb083c10ffb))


## [0.0.17](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/compare/v0.0.16..v0.0.17) - 2024-12-19

### ⚙️ Miscellaneous Tasks

- *(Docker)* Arm64 - ([ba6afda](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/ba6afda4e9a9831368a972e0ec26ca270d78a1b6))


## [0.0.16](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/compare/v0.0.15..v0.0.16) - 2024-12-19

### ⚙️ Miscellaneous Tasks

- *(docker)* Refine - ([ee749fc](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/ee749fceeb9df60bafdbc455950dfa14494ebb81))


## [0.0.15](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/compare/v0.0.14..v0.0.15) - 2024-12-19

### ⚙️ Miscellaneous Tasks

- *(workflows)* Test - ([f36e0ac](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/f36e0ac273ee95cb9d1b4c53160ce9d72cc0ad1d))


## [0.0.14](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/compare/v0.0.13..v0.0.14) - 2024-12-19

### ⚙️ Miscellaneous Tasks

- *(workflows)* Test - ([a3bb705](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/a3bb705bf8feb3f56b6a15c462566ad6b3a6c621))


## [0.0.13](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/compare/v0.0.12..v0.0.13) - 2024-12-19

### ⚙️ Miscellaneous Tasks

- *(workflows)* Test - ([113eb11](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/113eb11db86bb33d7839a316d8222236435f2c61))


## [0.0.12](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/compare/v0.0.11..v0.0.12) - 2024-12-19

### ⚙️ Miscellaneous Tasks

- *(workflow)* Test - ([63a476f](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/63a476f8627dcaaab49a9d0dd03756e98cde787d))


## [0.0.11](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/compare/v0.0.10..v0.0.11) - 2024-12-19

### ⚙️ Miscellaneous Tasks

- *(workflow)* Triggering - ([d502a12](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/d502a12213e95c507a506b5db8bb6a387a0ef078))


## [0.0.10](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/compare/v0.0.9..v0.0.10) - 2024-12-19

### ⚙️ Miscellaneous Tasks

- *(docker)* Release environment - ([7ec9c40](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/7ec9c4014847639277a8da08a15884ea03148703))
- *(release)* Prep - ([f7894f7](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/f7894f72f6288c613159d436f0faefedd7a842a7))


## [0.0.9](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/compare/v0.0.8..v0.0.9) - 2024-12-19

### ⛰️  Features

- *(Docker)* Start; refactor(logging, settings): continue - ([ba3cc07](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/ba3cc070a329632bc394993e822162184e46d52a))
- Run starbridge within Docker - ([cf8c1ac](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/cf8c1aca01e514c52e7e8d7809cf7440a2bc2a78))


## [0.0.8](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/compare/v0.0.7..v0.0.8) - 2024-12-18

### 🐛 Bug Fixes

- *(inspector)* Remove old script - now callable via uv run starbridge mcp inspect - ([f74994c](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/f74994c640809bd135ee96a0054ea2e4a5a5a2c3))

### ⚙️ Miscellaneous Tasks

- *(devcontainer)* Complete - ([51489b6](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/51489b6f8a50081f6bcfeaa3cfa2d192f9baf191))
- *(devcontainer)* Continue - ([81c2079](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/81c20791c4529442cd0a819b36324362f7fd4ee8))


## [0.0.7] - 2024-12-18

### ⛰️  Features

- *(confluence)* More tools - ([a7cdb48](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/a7cdb48a6a9385964b0de7dfdf9c91dff98b9752))
- Listing spaces and creating pages in Confluence - ([7eb4828](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/7eb4828ea407f09ff598977dfe95927afae058fd))

### 🐛 Bug Fixes

- Prompt template - ([d58f669](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/d58f66920bd30a16f05519ddb7f67e153224df36))
- Health down in ci - ([1299a87](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/1299a87ce7752a08e62d37cc18476467b3280b51))
- Tools - ([6331cb7](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/6331cb760a81512348862737ce76547f7351cb0d))

### 🚜 Refactor

- *(mcp)* Cli - ([a51e0d2](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/a51e0d2d9880d5b0d3af0b6ac97c17e70771229e))
- Continue - ([74e8305](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/74e8305d26f41c189ea5f7ea4ec7ce2d76eacdf7))
- Simplify - ([a366a4e](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/a366a4e3235865ff68b7747696b69ffce5936ad0))

### 📚 Documentation

- *(setup)* Tweaks - ([8aeaca9](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/8aeaca9c61ad85a45cd7d0af74d167d584eff929))
- Simplify install - ([512356f](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/512356fd21a012f4ea05cb544b7fa6d4ff6895f8))
- Badges ([#8](https://github.com/orhun/git-cliff/issues/8)) - ([4533df8](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/4533df8613600d76f49374dad24c7dda1e148dd7))
- .env - ([f008988](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/f0089880f4981ff8bd68b17c903ecd8103d4cae9))

### 🧪 Testing

- Pytest.ini - ([c704f8a](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/c704f8a09191d51f1f2cd9c23b40c507813e9bf4))

### ⚙️ Miscellaneous Tasks

- *(codespace)* Some - ([5acd68d](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/5acd68d1db9bd8d4487f74fed0f6a235ac407657))
- Spike devcontainer - ([a1bdf98](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/a1bdf984179f3adaf43417947b61e8cbeab77d80))
- Publish permissions - ([a5bc070](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/a5bc0701b32f928c0690a21aab2818cbbee1430e))
- Logfire spike - ([7e356c0](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/7e356c05998c9cdc00352401125456f973b0b32c))
- Codecov badge - ([941350f](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/941350f3728e69e06f15a91e0a7af3d241a7b854))
- Codecov - ([d733a28](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/d733a28fe48e473c14373039a91feb1e45d9c593))
- Configure Renovate ([#3](https://github.com/orhun/git-cliff/issues/3)) - ([c3725e3](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/c3725e384667b7111ffb0dbd19354122b22f202f))
- More info - ([02d30f9](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/02d30f92441595d2205ff6a068cc4dae6ff20bf8))

### Other

- Continue - ([9df04f3](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/9df04f3a9b874e528847ffb62f91f3cd46fbe6f4))

### Release

- Prep - ([519787f](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/commit/519787f154f795fcf9b4f00c9c0b5e04bb613cea))

## New Contributors ❤️

* @helmut-hoffer-von-ankershoffen made their first contribution
* @renovate[bot] made their first contribution in [#5](https://github.com/helmut-hoffer-von-ankershoffen/starbridge/pull/5)

<!-- built with love in Berlin by Helmut Hoffer von Ankershoffen -->
