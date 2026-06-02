pkgname=argononed
pkgdesc='Script for the Argon One Raspberry Pi 4 case.'
pkgver='latest'
pkgrel='1'
arch=('aarch64')

url="https://github.com/colinjmatt/$pkgname"
depends=('i2c-tools' 'python')

# 1. Download the branch archive and rename it locally to prevent conflicts
source=("$pkgname-master.tar.gz::https://github.com/colinjmatt/$pkgname/archive/refs/heads/master.tar.gz")

# 2. Skip checksums, as the master branch will constantly change hashes
sha256sums=('SKIP')

package() {
        # 3. GitHub extracts branch archives to RepoName-BranchName
        cd "$srcdir/$pkgname-master"
        
        install -Dm755 "argononed.py" "$pkgdir/opt/argonone/bin/argononed.py"
        install -Dm755 "argonone-config" "$pkgdir/usr/bin/argonone-config"
        install -Dm644 "argononed.conf" "$pkgdir/opt/argonone/argononed.conf"
        install -Dm755 "argononed-poweroff.py" "$pkgdir/usr/lib/systemd/system-shutdown/$pkgname-poweroff"
        install -Dm644 "argononed.service" "$pkgdir/usr/lib/systemd/system/argononed.service"
}
