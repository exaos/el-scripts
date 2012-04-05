#!/usr/bin/env lua
require('yaml')

------------------------------------------------------------
-- DVCS settings
function os.capture(cmd, raw)
  local f = assert(io.popen(cmd, 'r'))
  local s = assert(f:read('*a'))
  f:close()
  if raw then return s end
  s = string.gsub(s, '^%s+', '')
  s = string.gsub(s, '%s+$', '')
  s = string.gsub(s, '[\n\r]+', ' ')
  return s
end

local vcs_tools = {
   git = { os.capture("which git"),
	   {"pull origin", "gc --aggressive --prune=now"} },
   git_svn = { os.capture("which git"), {"svn fetch", "svn rebase -l"} },
   hg  = { os.capture("which hg"),  {"pull", "update", } },
   bzr = { os.capture("which bzr"), {"pull", } },
   svn = { os.capture("which svn"), {"update", }},
}

------------------------------------------------------------
-- loop over repos
local repo_up = function (base,p,vcs)
   local n_dir = base.."/"..p
   for _,c in pairs(vcs.cmds) do
      local cmd = "cd "..n_dir.." && "..vcs.prog.." "..c
      print("\n===========================================")
      print("PATH: "..n_dir.."\nEXEC: "..vcs.prog.." "..c.."\n")
      local ret = os.execute(cmd)
      if ret ~= 0 then
	 return false, n_dir, c
      end
   end
   return true
end

local function up_repos_dir(path)
   local repos = yaml.load(assert(io.open(path.."/repos.yaml"),
				  "Failed to open config: repos.yaml!")
			   : read("*a"))
   local err_log = {}
   for k,v in pairs(vcs_tools) do
      if type(repos[k])=="table" and #repos[k]>0 then
	 local vcs = {prog=v[1]}
	 if type(repos.cmds)=="table" and #repos.cmds[k] > 0 then
	    vcs.cmds = repos.cmds[k]
	 else
	    vcs.cmds = v[2]
	 end
	 for _,p in pairs(repos[k]) do
	    local r_ok, path, cmd = repo_up(path,p,vcs)
	    if not r_ok then table.insert(err_log, {path, cmd}) end
	 end
      end
   end
   return err_log
end

local function print_errors(el)
   local n_err = 0
   print("------------------------------")
   for i = 1,#el do
      for j = 1,#el[i] do
	 n_err = n_err + 1
	 print("==> ERROR: No. "..tostring(n_err))
	 print("path: "..tostring(el[i][j][1]))
	 print("exec: "..tostring(el[i][j][2]))
      end
   end
   print("\nTotal errors: "..tostring(n_err))
end

------------------------------------------------------------
-- command line
if #arg>0 then
   local err_list = {}
   for i=1,#arg do
      local err = up_repos_dir(arg[i])
      if #err > 0 then table.insert(err_list, err) end
   end
   print_errors(err_list)
else
   print([=[Usage: repos-up [path1] [path2] [...]]=])
end

