# Fmind color scheme for bobthefish
# bobthefish reads each color_* value as: background foreground [set_color options].
# Every segment is defined, so the result does not depend on theme_color_scheme.
function bobthefish_colors -S -d 'Define Fmind color scheme for bobthefish'
  # bobthefish draws these four in a single segment, so they must share a background.
  set -x color_initial_segment_exit     f1f3f4 a50e0e --bold
  set -x color_initial_segment_private  f1f3f4 202124
  set -x color_initial_segment_su       f1f3f4 a50e0e --bold
  set -x color_initial_segment_jobs     f1f3f4 174ea6 --bold

  set -x color_path                     d2e3fc 202124
  set -x color_path_basename            d2e3fc 174ea6 --bold
  set -x color_path_nowrite             fad2cf a50e0e
  set -x color_path_nowrite_basename    fad2cf a50e0e --bold

  set -x color_repo                     ceead6 0d652d
  set -x color_repo_work_tree           f1f3f4 202124 --bold
  set -x color_repo_dirty               feefc3 934900
  set -x color_repo_staged              d2e3fc 174ea6

  set -x color_vi_mode_default          f1f3f4 202124 --bold
  set -x color_vi_mode_insert           ceead6 0d652d --bold
  set -x color_vi_mode_visual           feefc3 934900 --bold

  set -x color_vagrant                  d2e3fc 174ea6 --bold
  set -x color_k8s                      d2e3fc 174ea6 --bold
  set -x color_aws_vault                feefc3 934900 --bold
  set -x color_aws_vault_expired        fad2cf a50e0e --bold
  set -x color_username                 f1f3f4 174ea6 --bold
  set -x color_hostname                 f1f3f4 174ea6
  set -x color_screen                   ceead6 0d652d --bold
  set -x color_rvm                      fad2cf a50e0e --bold
  set -x color_node                     ceead6 0d652d --bold
  set -x color_virtualfish              d2e3fc 174ea6 --bold
  set -x color_virtualgo                d2e3fc 174ea6 --bold
  set -x color_desk                     d2e3fc 174ea6 --bold
  set -x color_nix                      d2e3fc 174ea6 --bold
end
