{
  description = "Rust crate for wtr";

  inputs = {
    flake-schemas.url = "https://flakehub.com/f/DeterminateSystems/flake-schemas/*";
    nixpkgs.url = "https://flakehub.com/f/NixOS/nixpkgs/*";
    rust-overlay = {
      url = "https://flakehub.com/f/oxalica/rust-overlay/0.1.*";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = { self, flake-schemas, nixpkgs, rust-overlay }:
    let
      overlays = [
        rust-overlay.overlays.default
        (final: prev: {
          rustToolchain = final.rust-bin.stable.latest.default.override { 
            extensions = [ "rust-src" ]; 
          };
        })
        (final: prev: {
          ncurses = prev.ncurses.overrideAttrs (old: {
            postFixup = (old.postFixup or "") + ''
              rm -fv $dev/lib/pkgconfig/tinfo.pc  \
                    $dev/lib/pkgconfig/tic.pc
            '';
          });
        })
      ];

      supportedSystems = [ "x86_64-linux" "aarch64-darwin" "x86_64-darwin" "aarch64-linux" ];
      forEachSupportedSystem = f: nixpkgs.lib.genAttrs supportedSystems (system: f {
        pkgs = import nixpkgs { inherit overlays system; };
      });

      sharedEnv = pkgs: with pkgs.lib; {
        LLVM_SYS_180_PREFIX = "${pkgs.llvm_18.dev}";
        RUST_LOG = "debug";
        RUST_BACKTRACE = "1";
        RUST_SRC_PATH = "${pkgs.rustToolchain}/lib/rustlib/src/rust/library";
        
        # Enhanced library configuration
        PKG_CONFIG_PATH = makeSearchPath "lib/pkgconfig" [
          pkgs.libffi.dev
          pkgs.libxml2.dev
          pkgs.zlib.dev
          pkgs.openssl.dev
        ];
        
        LIBFFI_INCLUDE_DIR = "${pkgs.libffi.dev}/include";
        LIBFFI_LIB_DIR = "${pkgs.libffi}/lib";
        
        # macOS-specific linking flags
        NIX_LDFLAGS = optionalString pkgs.stdenv.isDarwin 
          "-L${pkgs.libffi}/lib -L${pkgs.libiconv}/lib";
      };
    in {
      schemas = flake-schemas.schemas;

      devShells = forEachSupportedSystem ({ pkgs }: {
        default = pkgs.mkShell.override { 
          stdenv = if pkgs.stdenv.isDarwin then pkgs.clangStdenv else pkgs.stdenv; 
        } {
          inputsFrom = [ self.packages.${pkgs.system}.default ];

          packages = with pkgs; [
            cargo-bloat
            cargo-edit
            cargo-outdated
            cargo-udeps
            cargo-watch
            rust-analyzer
            git
            jq
            nixpkgs-fmt
            zsh
          ];

          env = sharedEnv pkgs;

          shellHook = ''
            echo "🦀 Rust Development Environment"
            echo "=================================="
            echo "Rust version: $(rustc --version 2>/dev/null || echo 'Installing...')"
            echo "Ready for Rust development! 🚀"
          '';
        };
      });

      packages = forEachSupportedSystem ({ pkgs }: {
        default = let

          commonBuildInputs = with pkgs; [
            libffi
            libffi.dev
            libxml2
            libxml2.dev
            zlib
            zlib.dev
            libiconv
            llvm_18
            llvm_18.dev
            llvmPackages_18.libunwind
            openssl
            openssl.dev
            clang_18
            lld_18
          ];

          commonNativeBuildInputs = with pkgs; [
            pkg-config
            cmake
            gnumake
          ];

          rustPlatform = pkgs.makeRustPlatform {
            cargo = pkgs.rustToolchain;
            rustc = pkgs.rustToolchain;
          };
        in (rustPlatform.buildRustPackage.override { 
          stdenv = if pkgs.stdenv.isDarwin then pkgs.clangStdenv else pkgs.tdenv; 
        }) ({
          pname = "wtr";
          version = "0.1.0";
          src = builtins.path { path = ./.; name = "source"; };
          
          cargoLock = {
            lockFile = ./Cargo.lock;
          };

          nativeBuildInputs = commonNativeBuildInputs;
          buildInputs = commonBuildInputs;
        } // (sharedEnv pkgs));
      });
    };
}

