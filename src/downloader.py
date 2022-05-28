#!/usr/bin/python3
import subprocess
from sys import stdout
from mutagen.easyid3 import EasyID3

def get_audio_track(url):
    """Get the audio track from youtube url"""
    get_audio_track = subprocess.run(['yt-dlp', '-g', url], stdout=subprocess.PIPE)

    ytdl_g_out = get_audio_track.stdout.decode('utf-8')
    audio_track = ytdl_g_out.split()[1]
    return audio_track


def download_audio_parts(audio_track, track_info, outdir):
    """Download and encode audio to mp3"""
    if track_info['start'] == '-':
        start = "00:00"
    else:
        start = track_info['start']
    duration = track_info['duration']
    outfile = '/tmp/' + track_info['gendhing'] + '.mp3'
    cmd = ['ffmpeg', '-ss', start, '-i', audio_track, '-y', '-t', duration, '-ar', '44100', '-ac', '2', '-b:a', '192k', outfile]

    print("Downloading " + track_info['gendhing'])
    download_process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
    for line in download_process.stdout:
        if not line:
            break
        if 'speed=' in line:
            print("\r\t" + line.strip(), end="")
            #stdout.write("\t")
            stdout.flush()

    if download_process.returncode == 0:
        print("Download saved in " + outfile)
    else:
        print("error ");

    edit_metadata(outfile, track_info)

    copy_command = ['cp', outfile, outdir]
    subprocess.run(copy_command)


def edit_metadata(audio_file, track_info):
    """Change MP3 metadata"""
    track = EasyID3(audio_file)
    track['title'] = u"{0} - {1}".format(track_info['laras'], track_info['gendhing'])
    track['artist'] = u'Kridhamardawa'
    track['genre'] = track_info['gangsa']
    track.save()


if __name__ == '__main__':
    audio_info = {
        "gendhing": "Sarayuda",
        "laras": "SL My",
        "url": "https://youtu.be/WMXRiPk427g?t=18405",
        "start": "5:06:45",
        "end": "5:10:37",
        "duration": "3:52",
        "gangsa": "K.K Harjanegara",
        "downloaded": False
    }
    audio_track = get_audio_track(audio_info['url'])
    download_audio_parts(audio_track, audio_info, "/home/jikope/")
