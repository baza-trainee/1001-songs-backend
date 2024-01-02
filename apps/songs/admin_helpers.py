from django.core.files.base import ContentFile
from django.http import HttpResponseRedirect
from apps.songs.models import Song, SongLocation, SongDetail, SongMedia


def copy_song(request, song_id) -> HttpResponseRedirect:
    """
       Copies a song with the given identifier and creates a new record with a modified title.

       Args:
           request: HTTP request.
           song_id (int): The identifier of the song to copy

       Returns:
           HttpResponseRedirect: Redirects to the song administration page.
       """
    old_song = Song.objects.get(id=song_id)

    new_title = old_song.title + " - Copy"
    counter = 1
    while Song.objects.filter(title=new_title).exists():
        new_title = old_song.title + f" - Copy ({counter})"
        counter += 1

    new_song = Song.objects.create(
        title=new_title,
        recording_date=old_song.recording_date,
        performers=old_song.performers,
        collectors=old_song.collectors,
        source=old_song.source,
    )

    if hasattr(old_song, 'location'):
        old_location = old_song.location
        SongLocation.objects.create(
            song=new_song,
            country=old_location.country,
            region=old_location.region,
            district_center=old_location.district_center,
            administrative_code=old_location.administrative_code,
            ethnos=old_location.ethnos,
            ethnographic_district=old_location.ethnographic_district,
            city_ua=old_location.city_ua,
            city_eng=old_location.city_eng,
            unofficial_name_city=old_location.unofficial_name_city,
            recording_location=old_location.recording_location,
        )

    if hasattr(old_song, 'details'):
        old_details = old_song.details
        SongDetail.objects.create(
            song=new_song,
            incipit=old_details.incipit,
            genre_cycle=old_details.genre_cycle,
            poetic_text_genre=old_details.poetic_text_genre,
            texture=old_details.texture,
        )

    old_song_media = SongMedia.objects.filter(song=old_song)
    for media in old_song_media:
        if media.image and hasattr(media.image, 'file'):
            old_image = media.image
            old_image.open()
            new_media = SongMedia.objects.create(
                song=new_song,
            )
            new_media.image.save(
                old_image.name,
                ContentFile(old_image.read())
            )
            old_image.close()
        else:

            SongMedia.objects.create(
                song=new_song,
            )

    return HttpResponseRedirect('/admin/songs/song/')
