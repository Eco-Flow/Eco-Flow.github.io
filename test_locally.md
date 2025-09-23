### Install Jekyll

Changes to the website are not visible until they have been pushed, merged and deployed. Using Jeckyll, it is possbile to preview the website before commiting changes.

To test GitHub pages locally on Mac with Jeckyll, follow the next steps:

#### Step 1: Install Homebrew

If not installed:

```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

#### Step 2: Install chruby and the latest Ruby with ruby-install

Install `chruby` and `ruby-install` with Homebrew:

```
brew install chruby ruby-install
```

Install the latest stable version of Ruby (supported by Jekyll):

```
ruby-install ruby 3.4.1
```

This will take a few minutes, and once it’s done, configure your shell to automatically use `chruby`:

```
echo "source $(brew --prefix)/opt/chruby/share/chruby/chruby.sh" >> ~/.zshrc
echo "source $(brew --prefix)/opt/chruby/share/chruby/auto.sh" >> ~/.zshrc
echo "chruby ruby-3.4.1" >> ~/.zshrc # run 'chruby' to see actual version
```

Quit and relaunch Terminal, then check that everything is working:

```
ruby -v
```

It should show ruby 3.4.1 (2024-12-25 revision 48d4efcb85) or a newer version.

### Step 3: Install Jekyll

Once Ruby is installed, install the latest Jekyll gem:

```
gem install jekyll
```

### Step 4: Build site locally

Navigate to the location of the page repository (where the `Gemfile` is), and run:

```
bundle install
```

Once everything is installed, run your Jeckyll site locally:

```
bundle exec jekyll server
```

To preview the site, navigate to [http://localhost:4000](http://localhost:4000).
